from veadk.cloud.cloud_app import CloudApp

# the application name specified in the deploy command of 'vefaas-app-name'
# veadk deploy --access-key YOUR_AK --secret-key YOUR_SK --vefaas-app-name=youragentname --use-adk-web
THE_APPLICATION_NAME_TO_DELETE = "samplexxx"


def main() -> None:
    cloud_app = CloudApp(vefaas_application_name="THE_APPLICATION_NAME_TO_DELETE")
    cloud_app.delete_self()


if __name__ == "__main__":
    main()
