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

       stage("Unit tests") {
          when{
            expression{params.UNIT_TESTS == true}
          }
          steps {
              parallel(
                "Windows": {
                    node(label: 'Windows') {
                        deleteDir()
                        unstash "Source"
                        bat "${env.TOX}  -e jenkins"
                        junit 'reports/junit-*.xml'

                    }
                },
                "Linux": {
                    node(label: "!Windows") {
                        deleteDir()
                        unstash "Source"
                        withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {
                            sh "${env.TOX}  -e jenkins"
                        }
                        junit 'reports/junit-*.xml'
                    }
                }
              )
          }
        }
        stage("Packaging") {
            when{
                expression{params.PACKAGE == true}
            }
            steps {
                parallel(
                        "Windows Wheel": {
                            node(label: "Windows") {
                                deleteDir()
                                unstash "Source"
                                bat "${env.PYTHON3} setup.py bdist_wheel --universal"
                                archiveArtifacts artifacts: "dist/**", fingerprint: true
                            }
                        },
                        "Windows CX_Freeze MSI": {
                            node(label: "Windows") {
                                deleteDir()
                                unstash "Source"
                                bat """ ${env.PYTHON3} -m venv .env
                              call .env/Scripts/activate.bat
                              pip install -r requirements.txt
                              pip freeze
                              ${env.PYTHON3} cx_setup.py bdist_msi --add-to-path=true
                              """

                                dir("dist"){
                                    stash includes: "*.msi", name: "msi"
                                }

                            }
                            node(label: "Windows") {
                                deleteDir()
                                git url: 'https://github.com/UIUCLibrary/ValidateMSI.git'
                                unstash "msi"
                                // validate_msi.py

                                bat """
                      ${env.PYTHON3} -m venv .env
                      call .env/Scripts/activate.bat
                      pip install setuptools --upgrade
                      pip install -r requirements.txt
                      python setup.py install

                      echo Validating msi file(s)
                      FOR /f "delims=" %%A IN ('dir /b /s *.msi') DO (
                        python validate_msi.py ^"%%A^" frozen.yml
                        if not %errorlevel%==0 (
                          echo errorlevel=%errorlevel%
                          exit /b %errorlevel%
                          )
                        )
                      """
                                archiveArtifacts artifacts: "*.msi", fingerprint: true
                            }
                        },
                        "Source Release": {
                            deleteDir()
                            unstash "Source"
                            sh "${env.PYTHON3} setup.py sdist"
                            archiveArtifacts artifacts: "dist/**", fingerprint: true
                        }
                )
            }
        }
     }
  }
