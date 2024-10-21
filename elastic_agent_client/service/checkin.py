#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
import asyncio
import functools
import logging
from asyncio import CancelledError, Task, sleep
from typing import Any, Optional

import elastic_agent_client.generated.elastic_agent_client_pb2 as proto
from elastic_agent_client.client import V2
from elastic_agent_client.handler.checkin import BaseCheckinHandler
from elastic_agent_client.util.async_tools import AsyncQueueIterator, BaseService
from elastic_agent_client.util.logger import convert_agent_log_level, logger, set_logger


class CheckinV2Service(BaseService):
    name = "checkinV2"
    CHECKIN_INTERVAL = 5

    def __init__(self, client: V2, checkin_handler: BaseCheckinHandler):
        super().__init__(client, "checkinV2")
        logger.debug(f"Initializing the {self.name} service")
        self.client = client
        self.checkin_handler = checkin_handler
        self._send_checkins_task: Optional[Task[Any]] = None
        self._receive_checkins_task: Optional[Task[Any]] = None

    def stop(self):
        super().stop()
        if self._send_checkins_task:
            logger.info(f"Cancelling task: {self._send_checkins_task.get_name()}")
            self._send_checkins_task.cancel()
        if self._receive_checkins_task:
            logger.info(f"Cancelling task: {self._receive_checkins_task.get_name()}")
            self._receive_checkins_task.cancel()

    async def _run(self):
        logger.info(f"Starting {self.name} service")
        if self.client.client is None:
            msg = "gRPC client is not yet set"
            raise RuntimeError(msg)
        send_queue: asyncio.Queue = asyncio.Queue()
        checkin_stream = self.client.client.CheckinV2(AsyncQueueIterator(send_queue))

        send_checkins_task = asyncio.create_task(
            self.send_checkins(send_queue), name="Checkin Writer"
        )
        receive_checkins_task = asyncio.create_task(
            self.receive_checkins(checkin_stream), name="Checkin Reader"
        )
        send_checkins_task.add_done_callback(functools.partial(self._callback))
        receive_checkins_task.add_done_callback(functools.partial(self._callback))

        self._send_checkins_task = send_checkins_task
        self._receive_checkins_task = receive_checkins_task

        logger.debug(f"Running {self.name} service loop")
        done, pending = await asyncio.wait(
            [send_checkins_task, receive_checkins_task],
            return_when=asyncio.FIRST_EXCEPTION,
        )

        for task in pending:
            task.cancel()
            try:
                await task
            except CancelledError:
                logger.error("Task did not handle cancellation gracefully")

        # Separated these two to log all errors if both tasks error out together
        # Which is unlikely, but it's cheap to do it the way I did
        for task in done:
            if not task.cancelled() and task.exception():
                logger.error(
                    f"Task {task.get_name()} terminated due to exception:",
                    exc_info=task.exception(),
                )

        for task in done:
            if not task.cancelled():
                task_exception = task.exception()
                if task_exception:
                    raise task_exception

    async def send_checkins(self, send_queue):
        while self.running:
            if send_queue.empty():
                await self.do_checkin(send_queue)
            # Sleep if still running
            if self.running:
                await sleep(self.CHECKIN_INTERVAL)

    async def receive_checkins(self, checkin_stream):
        checkin: proto.CheckinExpected
        logger.info(f"{self.name} service is listening for check-in events")
        async for checkin in checkin_stream:
            logger.debug("Received a check-in event from CheckinV2 stream")
            await self.apply_expected(checkin)

    async def apply_expected(self, checkin: proto.CheckinExpected):
        if self.client.units and self.client.component_idx == checkin.component_idx:
            change_detected = False
            expected_units = [
                (unit.id, unit.config_state_idx, unit.log_level)
                for unit in checkin.units
            ]
            current_units = [
                (unit.id, unit.config_idx, unit.log_level) for unit in self.client.units
            ]
            for current_unit in current_units:
                if current_unit not in expected_units:
                    change_detected = True
                    break

            for expected_unit in expected_units:
                if expected_unit not in current_units:
                    change_detected = True
                    break

            if not change_detected:
                logger.debug("No change detected")
                return

        logger.debug("Detected change in units")
        self.client.agent_info = proto.AgentInfo(
            id=checkin.agent_info.id,
            version=checkin.agent_info.version,
            snapshot=checkin.agent_info.snapshot,
        )
        self.client.sync_component(checkin)
        self.client.sync_units(checkin)
        logger.debug("Calling apply_from_client with new units")
        self.pre_process_units()
        await self.checkin_handler.apply_from_client()

    def pre_process_units(self):
        logger.debug("Pre-processing units")
        if self.client.units is None:
            logger.debug("No units found")
            return

        outputs = [
            unit
            for unit in self.client.units
            if unit.unit_type == proto.UnitType.OUTPUT
        ]

        if len(outputs):
            unit = outputs[0]

            log_level = unit.log_level
            if log_level:
                # Convert the UnitLogLevel to the corresponding Python logging level
                python_log_level = convert_agent_log_level(log_level)
                logger.info(
                    f"Updating log level to {logging.getLevelName(python_log_level)}"
                )
                set_logger(log_level=python_log_level)
            else:
                logger.debug("No log level found for the output unit")
        else:
            logger.info("No outputs found")

    async def do_checkin(self, send_queue):
        if self.client.units is None:
            return
        logger.debug("Doing a check-in")
        units_observed = [unit.to_observed() for unit in self.client.units]

        if not self.client.version_info_sent and self.client.version_info:
            version_info = proto.CheckinObservedVersionInfo(
                name=self.client.version_info.name,
                meta=self.client.version_info.meta,
                build_hash=self.client.version_info.build_hash,
            )
        else:
            version_info = None
        supports: list[str] = []
        msg = proto.CheckinObserved(
            token=self.client.token,
            units=units_observed,
            version_info=version_info,
            features_idx=self.client.features_idx,
            component_idx=self.client.component_idx,
            supports=supports,
        )
        await send_queue.put(msg)
        self.client.version_info_sent = True
