from pytest_kind import KindCluster
from cloudkeeper.args import ArgumentParser
from cloudkeeper_plugin_k8s import KubernetesCollectorPlugin


def test_pod_default_namespace(kind_cluster):
    # test setup
    kind_cluster.kubectl("delete", "-f", "test/examples/Pod.yaml", "--ignore-not-found")
    kind_cluster.kubectl("apply", "-f", "test/examples/Pod.yaml")

    ArgumentParser.args.k8s_config = str(kind_cluster.kubeconfig_path)
    ArgumentParser.args.k8s_context = [kind_cluster.name]
    kcp = KubernetesCollectorPlugin()
    kcp.collect()

    assert kcp.graph.search_first_all({'resource_type': "kubernetes_pod",
                                       "name": "testpod"}) is not None
