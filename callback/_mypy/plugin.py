from typing import Callable, Optional

from mypy.plugin import Plugin, MethodSigContext
from mypy.types import CallableType


class CallbackRegistryType(Plugin):
    def get_method_signature_hook(self, fullname: str
                                  ) -> Optional[Callable[[MethodSigContext], CallableType]]:
        if fullname == 'callback.registry.CallbackRegistry.__iadd__':
            return CallbackRegistryType._handle_iadd_isub
        if fullname == 'callback.registry.CallbackRegistry.__isub__':
            return CallbackRegistryType._handle_iadd_isub

        if fullname == 'callback.registry.CallbackRegistry.__call__':
            return CallbackRegistryType._handle_call

        return None

    @staticmethod
    def _handle_call(ctx: MethodSigContext) -> CallableType:
        target_method: CallableType = ctx.type.args[0]
        assert isinstance(target_method, CallableType)

        return CallableType(
            arg_types=target_method.arg_types[1:],
            arg_kinds=target_method.arg_kinds[1:],
            arg_names=target_method.arg_names[1:],
            fallback=ctx.api.named_type('function'),
            ret_type=target_method.ret_type
        )

    @staticmethod
    def _handle_iadd_isub(ctx: MethodSigContext) -> CallableType:
        target_method: CallableType = ctx.type.args[0]
        assert isinstance(target_method, CallableType)

        names = list(target_method.arg_names)
        names[0] = None

        simplified_target = CallableType(
            arg_types=target_method.arg_types,
            arg_kinds=target_method.arg_kinds,
            arg_names=names,
            fallback=ctx.api.named_type('function'),
            ret_type=target_method.ret_type
        )

        return CallableType(
            arg_types=[simplified_target],
            arg_names=['other'],
            arg_kinds=[0],
            ret_type=ctx.type,
            fallback=ctx.api.named_type('function')
        )


def plugin(version: str):
    return CallbackRegistryType
