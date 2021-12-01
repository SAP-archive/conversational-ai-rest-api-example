#!/usr/bin/env groovy
@Library(['piper-lib', 'piper-lib-os', 'ml-cai-mario']) _

def FAILED_STAGE = 'Unknown'
def BADGE_MAP = [
    quality: [def qualityBadge, "Quality"], tests: [def testsBadge, "Tests"],
    checkmarx: [def checkmarxBadge, "Checkmarx"], xmake:[def xMakeBuildBadge, "Xmake Build"],
    documentation: [def documentation, "Documentation"]
]
def STATUS_MAP = [SUCCESS: 'passing', FAILURE: 'failing', UNSTABLE: 'unstable', ABORTED: 'aborted']

pipeline {
    agent { label 'slave' }
    options {
        skipDefaultCheckout()
        disableConcurrentBuilds()
    }
    stages {
        stage('Prepare') {
            steps {
                checkout scm
                setupPipelineEnvironment script: this
                sh 'mkdir -p ${WORKSPACE}/reports'
                script{
                    env.VERSION_TXT = readFile 'version.txt'
                    env.FAILED_STAGE = 'UNKNOWN'
                }
                initBadges(BADGE_MAP)
            }
        }
        stage('Quality') {
            failFast false
            parallel {
                stage('PyLint') {
                    steps {
                        durationMeasure(script: this, measurementName: 'pylint_duration') {
                            dockerExecute(script: this, dockerImage: 'docker.wdf.sap.corp:50001/com.sap.cai/python-dev:1.0.1-20200924171216') {
                                sh "pylint --rcfile=.pylintrc --output-format=parseable **/*.py | tee reports/pylint.log"
                            }
                        }
                    }
                    post {
                        always {
                            pythonChecksPublishResults()
                        }
                    }
                }
                stage('Safety') {
                    steps {
                        script {
                            sh "docker run -v ${env.WORKSPACE}/reports:/usr/src/app/reports docker.wdf.sap.corp:50001/com.sap.cai/python-dev:1.0.1-20200924171216 /bin/bash -c 'pip3 install safety;\
                                safety check | tee reports/safety.txt'"
                        }
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: '**/reports/safety.txt', allowEmptyArchive: true
                            testsPublishResults script: this, html: [
                                allowEmpty: true,
                                archive: true,
                                file: '**/reports/safety.txt'
                            ]
                        }
                    }
                }
            }
            post {
                always {
                    setBadgeStatus(BADGE_MAP['quality'], STATUS_MAP["${currentBuild.currentResult}"])
                }
            }
        }
        stage('Tests') {
            steps {
                sh 'make test'
            }
            post {
                always {
                    testsPublishResults(
                        script: this,
                        cobertura: [
                            active:true,
                            allowEmptyResults:true,
                            archive:true,
                            pattern: '**/reports/coverage/coverage.xml'
                        ],
                        html: [
                            active:true,
                            allowEmptyResults:true,
                            archive:true,
                            name: 'pytest',
                            path: '**/reports/coverage/html'
                        ],
                        junit: [
                            active:true,
                            allowEmptyResults:true,
                            archive: true,
                            pattern: '**/reports/junit.xml',
                            updateResults: true
                        ]
                    )
                    junit 'reports/junit.xml'
                    setBadgeStatus(BADGE_MAP['tests'], STATUS_MAP["${currentBuild.currentResult}"])
                }
            }
        }
//         stage('Checkmarx') {
//             when {
//                 branch 'master'
//             }
//             steps {
//                 checkmarxExecuteScan script: this
//             }
//             post {
//                 always {
//                     setBadgeStatus(BADGE_MAP['checkmarx'], STATUS_MAP["${currentBuild.currentResult}"])
//                 }
//             }
//         }
        stage('xMake Build') {
            when {
                branch 'master'
            }
            steps {
                lock(resource: "${env.JOB_NAME}/10", inversePrecedence: true) {
                    milestone 10
                    artifactPrepareVersion script: this
                    executeBuild script: this, buildType: 'xMakeStage', xMakeBuildQuality: 'Release'
                    executeBuild script: this, buildType: 'xMakePromote', xMakeBuildQuality: 'Release'
                }
            }
            post {
                always {
                    setBadgeStatus(BADGE_MAP['xmake'], STATUS_MAP["${currentBuild.currentResult}"])
                }
            }
        }
        stage('Documentation') {
            when {
                branch 'master'
            }
            steps {
                dockerExecute(script: this, dockerImage: 'docker.wdf.sap.corp:50001/com.sap.cai/python-dev:1.0.1-20200924171216', dockerOptions: "--user='root'") {
                    sh """
                        pip3 install -r requirements.txt
                        pip3 install pdoc3==0.7.4
                        pdoc3 dataset_translation --html --force --output-dir docs_temps
                       """
                }
                script {
                    sshagent(credentials: ["SSH_github"]) {
                        sh"""
                        git fetch origin gh-pages:gh-pages && git worktree add docs gh-pages
                        cp -r docs_temps/dataset_translation/. docs && cd docs
                        git add --all && git commit -m '[skip ci] Updating docs for ${env.VERSION_TXT}' && git push -u origin gh-pages || true
                        """
                    }
                }
            }
            post {
                always {
                    setBadgeStatus(BADGE_MAP['documentation'], STATUS_MAP["${currentBuild.currentResult}"])
                }
            }
        }
    }
    post {
        always {
            script {
                try {
                    sh 'mkdir ./down'
                    dir('./down') {
                        checkout scm
                        sh 'make down'
                    }
                } catch(e) {
                      echo e.getMessage()
                }
            }
            mailSendNotification script: this
            cleanWs()
        }
        failure {
            script {
                if(env.BRANCH_NAME == 'master'){
                    slackMessage('#D50000', "Failed Job: ${env.JOB_NAME} (${env.BUILD_NUMBER}) [Stage: ${env.FAILED_STAGE}]: ${env.BUILD_URL}")
                }
            }
        }
        success {
            script {
                if(env.BRANCH_NAME == 'master'){
                    slackMessage('#64DD17', "Successful Job: ${env.JOB_NAME} (${env.BUILD_NUMBER}): ${env.BUILD_URL}")
                }
            }
        }
    }
}
