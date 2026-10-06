# ☸️ Cheatsheet Kubernetes & Kubectl

## 🔍 Inspection & Logs

```bash
# Lister tous les Pods d'un Namespace avec IP et Nœud d'exécution
kubectl get pods -n <namespace> -o wide

# Afficher les logs d'un pod avec suivi en direct
kubectl logs -f <pod-name> -n <namespace>

# Descrption détaillée d'un pod (utile pour comprendre l'événement CrashLoopBackOff)
kubectl describe pod <pod-name> -n <namespace>
```

---

## 🛠️ Debug & Port Forwarding

```bash
# Rediriger un port d'un Service ou Pod vers la machine locale
kubectl port-forward svc/<service-name> 8080:80 -n <namespace>

# Lancer un pod temporaire de debug réseau (curl, netcat, dig)
kubectl run tmp-shell --rm -i --tty --image=nicolaka/netshoot -- /bin/bash
```
