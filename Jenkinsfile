pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv .venv-ci'
                sh '. .venv-ci/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt pytest'
            }
        }

        stage('Automated Tests') {
            steps {
                sh 'mkdir -p reports'
                sh '. .venv-ci/bin/activate && pytest -v --junitxml=reports/test-results.xml'
            }
            post {
                always {
                    junit testResults: 'reports/test-results.xml',
                          allowEmptyResults: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t student-academic-platform:v1.0.0 .'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/test-results.xml',
                             allowEmptyArchive: true
        }
    }
}
