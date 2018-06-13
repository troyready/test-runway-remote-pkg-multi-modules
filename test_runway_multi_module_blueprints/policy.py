#!/usr/bin/env python
"""Module with test IAM policy."""

from troposphere import Join, iam

import awacs.ec2
from awacs.aws import Allow, Policy, Statement

from stacker.blueprints.base import Blueprint
from stacker.blueprints.variables.types import CFNString


class IamPolicy(Blueprint):
    """Stacker blueprint for test iam policy."""

    VARIABLES = {
        'PolicySuffix': {'type': CFNString,
                         'description': 'Text to append to policy name'}
    }

    def create_template(self):
        """Create template (main function called by Stacker)."""
        template = self.template
        variables = self.get_variables()
        self.template.add_version('2010-09-09')
        self.template.add_description("Test Policy template v2")

        template.add_resource(
            iam.ManagedPolicy(
                'ManagedPolicy',
                Description='Sample managed policy.',
                ManagedPolicyName=Join(
                    '-',
                    ['testpolicyv2',
                     variables['PolicySuffix'].ref]
                ),
                Path='/',
                PolicyDocument=Policy(
                    Version='2012-10-17',
                    Statement=[
                        Statement(
                            Action=[awacs.ec2.DescribeInstances,
                                    awacs.ec2.DescribeTags,
                                    awacs.ec2.CreateTags],
                            Effect=Allow,
                            Resource=['*']
                        )
                    ]
                )
            )
        )


# Helper section to enable easy blueprint -> template generation
# (just run `python <thisfile>` to output the json)
if __name__ == "__main__":
    from stacker.context import Context
    print(IamPolicy('test',
                    Context({"namespace": "test"}),
                    None).to_json())
