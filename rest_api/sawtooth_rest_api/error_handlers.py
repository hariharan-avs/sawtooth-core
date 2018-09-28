# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
"""
Module: error_handlers.py
Usage: Module to define interface for route handlers to communicate specific
    response statuses they are interested in throwing an error on.
"""
# pylint: disable=no-name-in-module,import-error
# needed for the google protobuf imports to pass pylint
from sawtooth_rest_api.protobuf import client_transaction_pb2
from sawtooth_rest_api.protobuf import client_batch_submit_pb2
from sawtooth_rest_api.protobuf import client_state_pb2
from sawtooth_rest_api.protobuf import client_block_pb2
from sawtooth_rest_api.protobuf import client_batch_pb2
from sawtooth_rest_api.protobuf import client_receipt_pb2
import sawtooth_rest_api.exceptions as errors

class _ErrorTrap:
    # pylint: disable=too-few-public-methods
    # _ErrorTrap will be called through import
    """Provides an interface for route handlers to communicate specific
    response statuses they are interested in throwing an error on. Child
    classes should not define any methods, instead defining two class
    variables which the parent `check` method will reference. As `check` is
    a class method, there is no need to instantiate ErrorTraps.

    Attributes:
        trigger (int, enum): A protobuf enum status to check for.
        error (class): The type of error to raise.
    """
    trigger = None
    error = None

    @classmethod
    def check(cls, status):
        """Checks if a status enum matches the trigger originally set, and
        if so, raises the appropriate error.

        Args:
            status (int, enum): A protobuf enum response status to check.

        Raises:
            AssertionError: If trigger or error were not set.
            _ApiError: If the statuses don't match. Do not catch. Will be
                caught automatically and sent back to the client.
        """
        assert cls.trigger is not None, 'Invalid ErrorTrap, trigger not set'
        assert cls.error is not None, 'Invalid ErrorTrap, error not set'

        if status == cls.trigger:
            # pylint: disable=not-callable
            # cls.error will be callable at runtime
            raise cls.error()
    # pylint: disable=too-few-public-methods
    # _ErrorTrap will be called through import

class StatusResponseMissing(_ErrorTrap):
    """Interface for route handlers to communicate NO_RESOURCE error from
    batch submit protobuf - client batch status response.
    """
    trigger = client_batch_submit_pb2.ClientBatchStatusResponse.NO_RESOURCE
    error = errors.StatusResponseMissing
    # pylint: disable=too-few-public-methods
    # StatusResponseMissing extending _ErrorTrap


class BatchInvalidTrap(_ErrorTrap):
    """Interface for route handlers to communicate INVALID_BATCH error from
    batch submit protobuf - client batch submit response.
    """
    trigger = client_batch_submit_pb2.ClientBatchSubmitResponse.INVALID_BATCH
    error = errors.SubmittedBatchesInvalid
    # pylint: disable=too-few-public-methods
    # BatchInvalidTrap extending _ErrorTrap

class BatchQueueFullTrap(_ErrorTrap):
    """Interface for route handlers to communicate QUEUE_FULL error from
    batch submit protobuf - client batch submit response.
    """
    trigger = client_batch_submit_pb2.ClientBatchSubmitResponse.QUEUE_FULL
    error = errors.BatchQueueFull
    # pylint: disable=too-few-public-methods
    # BatchQueueFullTrap extending _ErrorTrap

class InvalidAddressTrap(_ErrorTrap):
    """Interface for route handlers to communicate INVALID_ADDRESS error from
    client state protobuf - client state get response.
    """
    trigger = client_state_pb2.ClientStateGetResponse.INVALID_ADDRESS
    error = errors.InvalidStateAddress
    # pylint: disable=too-few-public-methods
    # InvalidAddressTrap extending _ErrorTrap

class BlockNotFoundTrap(_ErrorTrap):
    """Interface for route handlers to communicate NO_RESOURCE error from
    block protobuf - client block get response.
    """
    trigger = client_block_pb2.ClientBlockGetResponse.NO_RESOURCE
    error = errors.BlockNotFound
    # pylint: disable=too-few-public-methods
    # BlockNotFoundTrap extending _ErrorTrap

class BatchNotFoundTrap(_ErrorTrap):
    """Interface for route handlers to communicate NO_RESOURCE error from
    batch protobuf - client batch get response.
    """
    trigger = client_batch_pb2.ClientBatchGetResponse.NO_RESOURCE
    error = errors.BatchNotFound
    # pylint: disable=too-few-public-methods
    # BatchNotFoundTrap extending _ErrorTrap

class TransactionNotFoundTrap(_ErrorTrap):
    """Interface for route handlers to communicate NO_RESOURCE error from
    transaction protobuf - client transaction get response.
    """
    trigger = client_transaction_pb2.ClientTransactionGetResponse.NO_RESOURCE
    error = errors.TransactionNotFound
    # pylint: disable=too-few-public-methods
    # BatchNotFoundTrap extending _ErrorTrap

class ReceiptNotFoundTrap(_ErrorTrap):
    """Interface for route handlers to communicate NO_RESOURCE error from
    receipt protobuf - client receipt get response.
    """
    trigger = client_receipt_pb2.ClientReceiptGetResponse.NO_RESOURCE
    error = errors.ReceiptNotFound
    # pylint: disable=too-few-public-methods
    # ReceiptNotFoundTrap extending _ErrorTrap

class StateNotFoundTrap(_ErrorTrap):
    """Interface for route handlers to communicate NO_RESOURCE error from
    state protobuf - client state get response.
    """
    trigger = client_state_pb2.ClientStateGetResponse.NO_RESOURCE
    error = errors.StateNotFound
    # pylint: disable=too-few-public-methods
    # StateNotFoundTrap extending _ErrorTrap

class InvalidAddressListTrap(_ErrorTrap):
    """Interface for route handlers to communicate INVALID_ADDRSS error from
    state protobuf - client state list response.
    """
    trigger = client_state_pb2.ClientStateListResponse.INVALID_ADDRESS
    error = errors.InvalidStateAddress
    # pylint: disable=too-few-public-methods
    # InvalidAddressListTrap extending _ErrorTrap
