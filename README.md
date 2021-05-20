# IoTRecorder2TextAidCloud
This repo is for cc project

## How to run

### 0. create virtual env
1. [install virualenv](https://virtualenv.pypa.io/en/latest/installation.html "Title"): sudo pip3 install virtualenv
2. create env by :virtualenv env

### 1. Google Cloud Setup
1. In the Cloud Console, on the project selector page, select or create a Cloud project.
2. Make sure that billing is enabled for your Google Cloud project.
3. Enable the Cloud IoT Core and Cloud Pub/Sub APIs. [Enable APIs](https://console.cloud.google.com/flows/enableapi?apiid=cloudiot.googleapis.com,pubsub&_ga=2.87379615.606901808.1589575300-1724261215.1588892683 "Title")
4. [Get authentication to the GCP API](https://cloud.google.com/docs/authentication/getting-started "Title")
### 2. Setup your local environment

1. [Install and initialize the Cloud SDK](https://cloud.google.com/sdk/docs/ "Title")
2. Clone this repo : https://github.com/fayexu/IoTRecorder2TextAidCloud. 
3. Change current directory to this repo folder
4. Download [Google's CA root certificate](https://pki.goog/roots.pem "Title") into the same directory. You can optionally set the location of the certificate with the --ca_certs flag.

### 3. Create a new Registry
1. Go to Google Cloud Console. If a project is not already created, create a new project.

2. Go to the [Google Core IoT module](https://console.cloud.google.com/iot?_ga=2.52683439.606901808.1589575300-1724261215.1588892683 "Title") in your project. 

3. Click Create registry.
* Name: my-registry
* Region: us-central1
4.  In the Default telemetry topic dropdown list, select Create a topic.
* In the Create a topic dialog, enter my-device-events in the Name field.
* Click Create in the Create a topic dialog
* The Device state topic and Certificate value fields are optional, so leave them blank.
5. Click Create on the Cloud IoT Core page.

### 4. Create a device private key pair
1. On your local machine, open up a terminal window and run the following command : 
```shell
openssl req -x509 -newkey rsa:2048 -keyout rsa_private.pem -nodes \
    -out rsa_cert.pem -subj "/CN=unused"
```

2. This will generate two files "rsa_private.pem" and "rsa_cert.pem"

### 5. Create a new device
1. On the Registries page, select my-registry.

2. Select the Devices tab and click Create a device.

3. Enter my-device for the Device ID.

4. Select Allow for Device communication.

5. Add the public key information to the Authentication fields.

* Copy the contents of rsa_cert.pem from the step above to the clipboard. Make sure to include the lines that say -----BEGIN CERTIFICATE----- and -----END CERTIFICATE-----.
* Select RS256_X509 for the Public key format.
* Paste the public key in the Public key value box.
* Click Add to associate the RS256_X509 key with the device.
6. The Device metadata field is optional; leave it blank.

7. Click Create.


### 6. Run the following command to create subscription(or on console)
```shell
gcloud pubsub subscriptions create \
    projects/PROJECT_ID/subscriptions/my-subscription \
    --topic=projects/PROJECT_ID/topics/my-device-events
```

### 7. Create an IAM User. 
1. Use Cloud Console to create a [service account](https://console.cloud.google.com/iam-admin/serviceaccounts/?_ga=2.153330239.606901808.1589575300-1724261215.1588892683 "Title"):
2. Click Select, then select a project to use for the service account.
3. Click Create service account.
- Name the account e2e-example and click Create.
- Select the role Project > Editor and click Continue.
- Click Create key.
- Under Key type, select JSON and click Create.
- Save this key to the same directory as the example Python files, and rename it service_account.json.

### 8. Creating a service account and setting the environment variable
```shell
export GOOGLE_APPLICATION_CREDENTIALS="xxx.json" (A JSON key file you saved in step 1.4)
```

### 9. create QLDB
1. Use AWS console to create a [QLDB](https://ap-southeast-1.console.aws.amazon.com/qldb/home?region=ap-southeast-1#getting-started "Title")
2. [Access QLDB](https://docs.aws.amazon.com/qldb/latest/developerguide/accessing.html "Title") 
3. QLDB [endpoints](https://docs.aws.amazon.com/general/latest/gr/qldb.html "Title")


### 10. p2p framework
https://github.com/macsnoeren/python-p2p-network
```shell
pip install p2pnetwork
```
### 11. run application
```shell
python app.py <project_id> <path_to_audio_file> <topic_id> <subscription_id> <bucket_id> <transcribe_job_name>
```
