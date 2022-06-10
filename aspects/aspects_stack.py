import sys

from aws_cdk import (
    Resource,
    Stack,
    Aspects, IAspect,
    RemovalPolicy,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_iam as iam,
    aws_sns as sns
)
from constructs import Construct
import jsii

@jsii.implements(IAspect)
class RoleChecker():

    # eliminate any instances of CfnRole
    # attach a specific role to Lambdas
    
    def visit(self, node):

        # print(f'{node} - {node.addr}', file=sys.stderr)
        print(node, file=sys.stderr)


        if not Resource.is_resource(node):
            print('  not a resource', file=sys.stderr)
            # return        

        if Construct.is_construct(node):
            print('  node.addr -> '+node.node.addr, file=sys.stderr)
        # else:
        #     print('  not a Construct', file=sys.stderr)



class AspectsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Aspects.of(self).add(RoleChecker())

        bucket = s3.Bucket(
            self,
            "aBucket",
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
            event_bridge_enabled=True,
            #**kms_params
        )

        topic = sns.Topic(self, 'aTopic')

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.SnsDestination(topic))




