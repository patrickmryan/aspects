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
    
    def __init__(self, handler_role=None):
        self.handler_role = handler_role

    def log(self, message, **kwargs):
        print(message, **kwargs, file=sys.stderr)
    
    def visit(self, construct):
        # eliminate any instances of CfnRole
        # attach a specific role to Lambdas

        self.log(f'me -> {str(construct)}, node-> {construct.node.id}, {str(construct.node)},  ({str(construct.__class__)})')
        # self.log('  my node -> '+str(construct.node.__class__))
        # self.log(dir(construct))
        # self.log(construct)
        
        self.log('  default - '+str(construct.node.default_child))

        kids = construct.node.children
        if not kids:
            self.log('  no children')
        else:
            self.log('  children')
            for kid in kids:
                self.log(f'    {str(kid)}, node-> {str(kid.node)}')

                if isinstance(kid, iam.Policy):
                    # kill off the policy
                    self.log(f'  trying to remove {str(kid)}')
                    construct.node.try_remove_child(kid.node.id)
            

        # verb = 'is' if Resource.is_resource(node) else 'is not'
        # self.log(f'  {verb} a resource')

        # if Construct.is_construct(node):
        #      self.log('  is a Construct')

        # if not isinstance(construct, s3.Bucket):
        #     return




        # self.log('role = '+str(node._notifications_handler_role))
        # node._notifications_handler_role = self.handler_role
        # self.log('role = '+str(node._notifications_handler_role))


class AspectsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role.from_role_name(self, 'HandlerRole', 's3_handler_role')

        # Aspects.of(self).add(RoleChecker(handler_role=role))

        bucket = s3.Bucket(
            self,
            "aBucket",
            notifications_handler_role=role
        )

        Aspects.of(self).add(RoleChecker(handler_role=role))  # was role

        topic = sns.Topic(self, 'aTopic')

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.SnsDestination(topic))




