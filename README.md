# k8s-api-calls
Simulate API calls do K8s inside a container using ServiceAccount's

## Create namespace
```sh
kubectl create namespace k8s-api-calls
```

## Service account
```yml
# cat service_account.yml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: "k8s-api-calls"
  namespace: "k8s-api-calls"
  labels:
    app: "k8s-api-calls"
```

```sh
kubectl apply -n k8s-api-calls -f service_account.yml
```


## Role
```yml
# cat role.yml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: "k8s-api-calls-role"
  namespace: "k8s-api-calls"
  labels:
    app: "k8s-api-calls"
rules:
  - apiGroups: [""]
    resources:
      - pods
    verbs:
      - list
      - get
```

```sh
kubectl apply -n k8s-api-calls -f role.yml
```


## Role Binding
```yml
# cat role_binding.yml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: "k8s-api-calls-rolebinding"
  namespace: "k8s-api-calls"
  labels:
    app: "k8s-api-calls"
subjects:
  - kind: ServiceAccount
    name: "k8s-api-calls"
    namespace: "k8s-api-calls"
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: "k8s-api-calls-role"
```

```sh
kubectl apply -n k8s-api-calls -f role_binding.yml
```

## Daemonset
```yml
# cat daemonset.yml
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: k8s-api-calls
  namespace: k8s-api-calls
  labels:
    app: k8s-api-calls
spec:
  selector:
    matchLabels:
      app: k8s-api-calls
  template:
    metadata:
      labels:
        app: k8s-api-calls
    spec:
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: k8s-api-calls
        image: marceloalmeida/k8s-api-calls:latest
        imagePullPolicy: Always
        tty: true
        livenessProbe:
          exec:
            command:
            - echo
            - alive
          failureThreshold: 3
          initialDelaySeconds: 60
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 500m
            memory: 200Mi
      serviceAccount: k8s-api-calls
      serviceAccountName: k8s-api-calls
      terminationGracePeriodSeconds: 30
```

```sh
kubectl apply -n k8s-api-calls -f daemonset.yml
```
