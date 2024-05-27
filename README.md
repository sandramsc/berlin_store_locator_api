# **Cloud Native REST API in Python on K8s**

## Development Process

1. Creating REST API in Python3 using Flask
2. Ran the REST API local 'district_id': args['district_id'],
            'dist_name': args['dist_name'],
            'stores': storesly.
3. Containerized the REST API
    1. Created Dockerfile
    2. Built Docker Image
    3. Ran Docker Container
4. Created ECR repository using Python3 Boto3 and pushed Docker Image to ECR
5. Created EKS cluster and Node groups
6. Created Kubernetes Deployments and Services using Python3


## **Tools & technologies used in this project**

- [x]  AWS: EKS, ECR
- [x]  Programmatic access and AWS configured with CLI
- [x]  Python3 
- [x]  Python Boto3 
- [x]  Docker and Kubectl installed
- [x]  Code editor (VScode)

## Challenges & Take away

- [x]  (challenge) I chose to create this REST API because a CLI tool I am building needs an API of this structure, but I did not find one in the short time of research I did so I chose to build one. The most challenging aspect was figuring out how to create nested fields (so they'd render in the UI via code as they do in the JSON file) and test the requests so they were all successfull.
 <div id="header" align="center">
  <img src="https://github.com/sandramsc/berlin_store_locator_api/assets/19821445/521f2564-bb7c-4c7c-8365-0ad758329a8a" width="1050" />
</div>

- [x]  (challenge) Since this API had a store field and a products field that were alll nested under the districts field, I needed to figure out a function that would enable users to GET, PUT, PATCH to any one field if they so desired to, this in part was tied to finding a solution to list the resource fields and then calling these in their respective requests. This took a couple of days and at the moment only the test for the PUT request is working as it should.
- [x]  (take away) It's a great thing that I am enjoying the processes of developing this tool as the challenges did certainly cause moment for pause and reconsideration in the wee hours of 4am when debugging and trying to find a fix unittests for the requests. It tought me that resiliance and consistency in working on a project project you enjoy is worth the challenge (and to take short breaks between debugging, helps with re-focusing and looking at the bug from different perspctives, which aided with finding a solution) and I learned how to create resources for netsed fields.

----------
- [x]  (challenge) Worked on degugging (over 8hrs) why the REST API wouldn't push to the ECR on AWS.

 <div id="header" align="center">
  <img src="https://github.com/sandramsc/berlin_store_locator_api/assets/19821445/c5dc4faa-ccb3-4859-ad7e-7f2ddf49d29d" width="1050" />
</div>
I had already:

- added access_id
- added access_key
- added region
- logged in successfully
- built the image
- added a tag
  
yet the image still wouldn't push. I'd also given the IAM user these permissions:

- AdministratorAccess
- AmazonEC2ContainerRegistryFullAccess
- AWSAppRunnerServicePolicyForECRAccess
- IAMUserChangePassword

***Most StackOverflow, GitHub related posts suggested to add the above in different ways, initially none would work for several hours 🥴.

- [x]  (take away) The challenge with ECR pushing underscored the intricacies of AWS IAM permissions and Docker interactions. This experience emphasized the need for careful consideration of AWS configurations and troubleshooting strategies, showcasing the importance of perseverance and resourcefulness in resolving technical hurdles.

## **Part 1: Deploying the Flask application locally**

### **Step 1: Clone the code**

Clone the code from the repository:

```
git clone berlin_store_locator_api
```

### **Step 2: Install dependencies**

```
pip3 install -r requirements.txt
```

### **Step 3: Run the application**

To run the application, navigate to the root directory of the project and execute the following command:

```
python3 app.py
```

This will start the Flask server on **`localhost:5000`**. Navigate to [http://localhost:5000/](http://localhost:5000/) on your browser to access the application.

## **Part 2: Dockerizing the Flask application**

### **Step 1: Created a Dockerfile**
### **Step 2: Built the Docker image**
### **Step 3: Ran the Docker container**

This will start the Flask server in a Docker container on **`localhost:5000`**. Navigate to [http://localhost:5000/](http://localhost:5000/) on your browser to access the application.

## **Part 3: Pushed the Docker image to ECR**

### **Step 1: Created an ECR repository**
### **Step 2: Push the Docker image to ECR**

## **Part 4: Created an EKS cluster and deploying the app using Python**

### **Step 1: Created an EKS cluster**
### **Step 2: Created a node group**
### **Step 3: Create deployment and service**

- Once this file is executed by running “python3 eks.py” deployment and service will be created.
- Confirm by running following commands:

```jsx
kubectl get deployment -n default (check deployments)
kubectl get service -n default (check service)
kubectl get pods -n default (to check the pods)
```

Once the pod is up and running, execute the port-forward to expose the service

```bash
kubectl port-forward service/<service_name> 5000:5000
```
