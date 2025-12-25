# Hello World Kubernetes Deployment

## พร้อม Jenkins CI, ArgoCD, และ Grafana Monitoring

โปรเจกต์นี้สาธิตการ deploy Hello World service บน Minikube พร้อมระบบ CI/CD และ Monitoring ครบวงจร

## 📁 โครงสร้างโปรเจกต์

```
pscp/
├── app/                          # Source code
│   ├── app.py                    # Flask Hello World application
│   └── requirements.txt          # Python dependencies
├── k8s/                          # Kubernetes manifests
│   ├── namespace.yaml            # Namespace definition
│   ├── deployment.yaml           # Deployment configuration
│   ├── service.yaml              # Service (NodePort)
│   └── configmap.yaml            # ConfigMap
├── argocd/                       # ArgoCD configurations
│   ├── application.yaml          # ArgoCD Application
│   └── project.yaml              # ArgoCD Project
├── monitoring/                   # Monitoring configurations
│   ├── service-monitor.yaml      # Prometheus ServiceMonitor
│   ├── grafana-dashboard.json    # Grafana Dashboard
│   └── grafana-configmap.yaml    # Dashboard ConfigMap
├── scripts/
│   └── setup.sh                  # Setup script
├── Dockerfile                    # Docker build file
├── Jenkinsfile                   # Jenkins CI pipeline
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Minikube installed
- kubectl installed
- Helm installed (สำหรับ Prometheus/Grafana)
- Docker installed

### 1. เริ่มต้นใช้งาน

```bash
# ให้สิทธิ์ execute script
chmod +x scripts/setup.sh

# รัน setup script
./scripts/setup.sh
```

### 2. Manual Setup (ทีละขั้นตอน)

#### 2.1 Start Minikube

```bash
minikube start --driver=docker --cpus=4 --memory=8192
```

#### 2.2 Build Docker Image

```bash
# ใช้ Minikube's Docker daemon
eval $(minikube docker-env)

# Build image
docker build -t hello-world:latest .
```

#### 2.3 Deploy Hello World

```bash
kubectl apply -f k8s/
```

#### 2.4 Install ArgoCD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# รอให้ ArgoCD พร้อม
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd

# Apply ArgoCD Application
kubectl apply -f argocd/
```

#### 2.5 Install Prometheus & Grafana

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

kubectl create namespace monitoring

helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
    --namespace monitoring \
    --set grafana.adminPassword=admin
```

---

## 🔄 Jenkins CI Flow

Jenkins Pipeline ทำงานดังนี้:

1. **Checkout** - ดึง source code จาก Git
2. **Update Message** - เปลี่ยนข้อความ Hello World ใน deployment
3. **Build Docker Image** - Build image ใหม่
4. **Test** - ทดสอบ container
5. **Update Manifest** - อัพเดท image tag ใน deployment.yaml
6. **Commit Changes** - Push กลับไป Git

### วิธีเปลี่ยนข้อความ Hello World

แก้ไขไฟล์ `Jenkinsfile`:

```groovy
environment {
    HELLO_MESSAGE = 'ข้อความใหม่ของคุณ!'
}
```

เมื่อ push ขึ้น Git, Jenkins จะ:

1. Build image ใหม่
2. Update deployment.yaml
3. ArgoCD จะ sync อัตโนมัติ

---

## 🌐 Access URLs

### Hello World Service

```bash
minikube service hello-world -n hello-world
```

### ArgoCD UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443

# เปิด browser: https://localhost:8080
# Username: admin
# Password:
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d
```

### Grafana

```bash
kubectl port-forward svc/prometheus-grafana -n monitoring 3000:80

# เปิด browser: http://localhost:3000
# Username: admin
# Password: admin
```

### Prometheus

```bash
kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090

# เปิด browser: http://localhost:9090
```

---

## 📊 Grafana Dashboard

Dashboard แสดงข้อมูลดังนี้:

| Panel          | Description                 |
| -------------- | --------------------------- |
| CPU Usage      | การใช้ CPU ของแต่ละ Pod (%) |
| Memory Usage   | การใช้ Memory ของแต่ละ Pod  |
| Running Pods   | จำนวน Pod ที่กำลังทำงาน     |
| Pod Restarts   | จำนวนครั้งที่ Pod restart   |
| Average CPU    | ค่าเฉลี่ย CPU (Gauge)       |
| Average Memory | ค่าเฉลี่ย Memory (Gauge)    |

### Import Dashboard

1. เปิด Grafana → Dashboards → Import
2. Upload file `monitoring/grafana-dashboard.json`
3. Select Prometheus datasource
4. Click Import

---

## 🔧 Useful Commands

```bash
# ดู pods ทั้งหมด
kubectl get pods -n hello-world

# ดู logs
kubectl logs -f deployment/hello-world -n hello-world

# ดู ArgoCD applications
kubectl get applications -n argocd

# ดู service
kubectl get svc -n hello-world

# Scale pods
kubectl scale deployment hello-world --replicas=3 -n hello-world

# Restart deployment
kubectl rollout restart deployment/hello-world -n hello-world
```

---

## 🏗️ Architecture

```
                    ┌─────────────┐
                    │   GitHub    │
                    │  Repository │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
   ┌──────────┐     ┌──────────┐     ┌──────────┐
   │ Jenkins  │────▶│  ArgoCD  │────▶│ Minikube │
   │   (CI)   │     │   (CD)   │     │  Cluster │
   └──────────┘     └──────────┘     └────┬─────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    ▼                     ▼                     ▼
              ┌──────────┐         ┌──────────┐         ┌──────────┐
              │  Hello   │         │Prometheus│         │ Grafana  │
              │  World   │◀───────▶│          │────────▶│Dashboard │
              │ Service  │         └──────────┘         └──────────┘
              └──────────┘
```

---

## 🎓 Learning Path

1. **เริ่มต้น**: รัน setup.sh และดู Hello World service
2. **ทดลอง CI**: แก้ไข HELLO_MESSAGE ใน Jenkinsfile และ push
3. **ดู ArgoCD**: สังเกตการ sync อัตโนมัติ
4. **Monitor**: ดู CPU/Memory ใน Grafana
5. **Scale**: ลอง scale pods และดูผลใน Grafana

---

## ❓ Troubleshooting

### Pod ไม่ขึ้น

```bash
kubectl describe pod -n hello-world
kubectl logs -f <pod-name> -n hello-world
```

### Image pull error

```bash
# ต้องใช้ Minikube's Docker
eval $(minikube docker-env)
docker build -t hello-world:latest .
```

### ArgoCD ไม่ sync

```bash
kubectl get applications -n argocd
argocd app sync hello-world
```

---

## 📝 License

MIT License
