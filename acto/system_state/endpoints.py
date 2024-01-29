"""Endpoints state model"""

import kubernetes
import kubernetes.client.models as kubernetes_models
import pydantic
from typing_extensions import Self

from acto.system_state.kubernetes_object import (
    KubernetesNamespacedDictObject,
    list_namespaced_object_helper,
)


class EndpointsState(KubernetesNamespacedDictObject):
    """Endpoints state object."""

    root: dict[str, kubernetes_models.V1Endpoints]

    @classmethod
    def from_api_client_namespaced(
        cls, api_client: kubernetes.client.ApiClient, namespace: str
    ) -> Self:
        data = list_namespaced_object_helper(
            kubernetes.client.CoreV1Api(api_client).list_namespaced_endpoints,
            namespace,
        )
        return cls.model_validate(data)

    def check_health(self) -> tuple[bool, str]:
        """Check Endpoints health"""
        return True, ""

    @pydantic.model_serializer
    def serialize(self):
        return {key: value.to_dict() for key, value in self.root.items()}
