import json
import boto3
import argparse
import widgets as w


# Checking to see if widget metric requires are cluster level or instance level.
# If the metric is instance level, associate all instances for instance level metrics
def add_metric(widJson, widgets, region, instanceList, clusterList):
    for widget in widgets:
        widget["properties"]['region'] = region
        if 'metrics' in widget["properties"]:
            if 'DBInstanceIdentifier' in widget["properties"]["metrics"][0]:
                for i, DBInstanceIdentifier in enumerate(instanceList):
                    if DBInstanceIdentifier['IsClusterWriter']:
                        instanceType = '|PRIMARY'
                    else:
                        instanceType = '|REPLICA'

                    if (i == 0):
                        widget["properties"]["metrics"][i].append(DBInstanceIdentifier['DBInstanceIdentifier'])
                        widget["properties"]["metrics"][i].append({"label":DBInstanceIdentifier['DBInstanceIdentifier']+instanceType})
                    else:
                        widget["properties"]["metrics"].append([".",".",".",DBInstanceIdentifier['DBInstanceIdentifier'],{"label":DBInstanceIdentifier['DBInstanceIdentifier']+instanceType}])

            else:
                for i, DBClusterIdentifier in enumerate(clusterList):
                    if (i == 0):
                        widget["properties"]["metrics"][i].append(DBClusterIdentifier)
                        widget["properties"]["metrics"][i].append({"label":DBClusterIdentifier})
                    else:
                        widget["properties"]["metrics"].append([".",DBClusterIdentifier,{"label":DBClusterIdentifier}])

        widJson["widgets"].append(widget)


# Main method
def main():
    # Command line arguments for user to pass
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True)
    parser.add_argument('--region', type=str, required=True)
    parser.add_argument('--clusterID', type=str, required=True)
    args = parser.parse_args()

    # DocumentDB Configurations
    docdbclient = boto3.client('docdb', region_name=args.region)

    clusterList = args.clusterID.split(',')
    instanceList = []
    for thisCluster in clusterList:
        response = docdbclient.describe_db_clusters(DBClusterIdentifier=thisCluster,Filters=[{'Name': 'engine','Values': ['docdb']}])
        for thisInstance in response["DBClusters"][0]["DBClusterMembers"]:
            instanceList.append(thisInstance)

    #instanceID = response["DBClusters"][0]["DBClusterMembers"]

    # CloudWatch client
    client = boto3.client('cloudwatch', region_name=args.region)

    # All widgets to be displayed on the dashboard
    widgets = [
        w.ClusterHeading,

        w.metricHelp,
        w.bestPractices,

        w.DBClusterReplicaLagMaximum,
        w.DatabaseCursorsTimedOut,
        w.VolumeWriteIOPS,
        w.VolumeReadIOPS,

        w.OpscountersInsert,
        w.OpscountersUpdate,
        w.OpscountersDelete,
        w.OpscountersQuery,

        w.InstanceHeading,

        w.CPUUtilization,
        w.DatabaseConnections,
        w.DatabaseCursors,

        w.BufferCacheHitRatio,
        w.IndexBufferCacheHitRatio,
        w.FreeableMemory,

        w.NetworkTransmitThroughput,
        w.NetworkReceiveThroughput,

        w.DocsInserted,
        w.DocsDeleted,
        w.DocsUpdated,
        w.DocsReturned,

        w.ReadLatency,
        w.WriteLatency,
        w.DiskQueueDepth,

        w.BackupStorageHeading,

        w.VolumeBytesUsed,
        w.BackupRetentionPeriodStorageUsed,
        w.TotalBackupStorageBilled
    ]

    # Deploy metrics
    add_metric(w.widget_json, widgets, args.region, instanceList, clusterList)

    # Converting python to json
    dashBody = json.dumps(w.widget_json)

    # Create dashboard
    client.put_dashboard(DashboardName=args.name, DashboardBody=dashBody)

    print("Your dashboard has been deployed! Proceed to CloudWatch to view your dashboard")


if __name__ == "__main__":
    main()
