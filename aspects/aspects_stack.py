import sys

from aws_cdk import (
    Resource,
    Stack,
    Aspects,
    IAspect,
    RemovalPolicy,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_iam as iam,
    aws_sns as sns,
)
from constructs import Construct
import jsii


@jsii.implements(IAspect)
class PolicyEliminator:
    def log(self, message, **kwargs):
        print(message, **kwargs, file=sys.stderr)

    def visit(self, construct):
        # eliminate any instances of iam.Policy

        policies = [
            kid.node.id
            for kid in construct.node.children
            if isinstance(kid, iam.Policy)
        ]

        for policy_id in policies:
            construct.node.try_remove_child(policy_id)


class AspectsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role.from_role_name(self, "HandlerRole", "s3_handler_role")

        Aspects.of(self).add(PolicyEliminator())

        bucket = s3.Bucket(self, "aBucket", notifications_handler_role=role)
        topic = sns.Topic(self, "aTopic")

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED, s3n.SnsDestination(topic)
        )
