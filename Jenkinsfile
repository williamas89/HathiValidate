pipeline {
    agent any
    parameters {
      string(name: "PROJECT_NAME", defaultValue: "Hathi Validate", description: "Name given to the project")
      booleanParam(name: "UNIT_TESTS", defaultValue: true, description: "Run Automated Unit Tests")
      booleanParam(name: "STATIC_ANALYSIS", defaultValue: true, description: "Run static analysis tests")
      booleanParam(name: "PACKAGE", defaultValue: true, description: "Create a Packages")
      booleanParam(name: "DEPLOY", defaultValue: false, description: "Deploy SCCM")
      booleanParam(name: "BUILD_DOCS", defaultValue: true, description: "Build documentation")
      booleanParam(name: "UPDATE_DOCS", defaultValue: false, description: "Update the documentation")
      string(name: 'URL_SUBFOLDER', defaultValue: "hathi_validate", description: 'The directory that the docs should be saved under')
    }
    stages {
       stage("Cloning Source") {
           agent any

           steps {
               deleteDir()
               checkout scm
               stash includes: '**', name: "Source", useDefaultExcludes: false

           }

       }
     }
  }
