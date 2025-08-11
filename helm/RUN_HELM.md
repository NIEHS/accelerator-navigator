# Run ChromaDB in Kubernetes with Helm

The following will add ChromaDB to Accelerator for testing/development purposes

Helm Chart: https://github.com/amikos-tech/chromadb-chart

A pre-packaged [test values](./test_values.yaml) file is included to align with the test framework

## Instructions

See [Chroma chart README](https://github.com/amikos-tech/chromadb-chart/blob/main/README.md) for details

### Install the Helm Chart

```shell

cd helm

helm repo add chroma https://amikos-tech.github.io/chromadb-chart/
helm repo update

```

The included [test values](test_values.yaml) has overrides that generally apply to 
development and integration tests.

If you are running this with Accelerator, you might want to install this into the same namespace. N.B. that 'k' is 
an alias for kubectl in this document.

```shell

k config set-context --current --namespace=accelerator-dev


```

The following command is using the accelerator namespace, so omit the -n flag or change the namespace if desired.

We want to provide a token that we can use for testing. Let's leave this out of the git repo! Set a value via a 
property override



```shell

k create secret generic chromadb-auth-custom --from-literal=token="my-token"

helm install chroma chroma/chromadb -n accelerator-dev --set chromadb.auth.existingSecret="chromadb-auth-custom" -f test_values.yaml

```

For the integration tests, you need to set that chromadb token value as an environment variable for your tests.

To test, given that you've set the context to the correct namespace, try this:

```shell

export CHROMA_TOKEN=$(kubectl get secret chromadb-auth-custom -o jsonpath="{.data.token}" | base64 --decode)

export CHROMA_HEADER_NAME=$(kubectl get configmap chroma-chromadb-token-auth-config -o jsonpath="{.data.CHROMA_AUTH_TOKEN_TRANSPORT_HEADER}")


```
