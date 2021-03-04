from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_route53 as route53
)


class ValhallaBotStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        lambda_function = _lambda.Function(
            self, 'Valhalla-Bot',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.AssetCode('lambda'),
            handler='app.handler',
        )
        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=lambda_function
        )