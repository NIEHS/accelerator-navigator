# accelerator-navigator
Accelerator support for Navigator

## Description

This is a set of codes, based on accelerator_core (https://github.com/NIEHS/accelerator-core), used to push data from 
accelerator into Navigator data sinks.

## Dev Notes

This starts with two main classes, which translates to task handlers within an Airflow DAG but can also be 
executed outside of Airflow.

* navigator_dissemination_crosswalk takes data from the accelerator schema and translates into a form suitable for ingest into Navigagtor
* navigator_target_dissemination takes prepared data and places it into the target

### Relevant Repos and Docs

* Accelerator Core Libraries (https://github.com/NIEHS/accelerator-core)
* Accelerator DAG repository (https://github.com/NIEHS/accelerator-dag)
* Accelerator Helm Charts (https://github.com/NIEHS/accelerator-helm)
