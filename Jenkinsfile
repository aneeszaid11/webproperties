pipeline {
    agent any

    environment {
        OUTPUT_DIR = "/data"
    }

    stages {
        stage('Run Script') {
            steps {
                sh '''
                    set -e

                    python redirect-check-1.py

                    if ls redirect_results*.xlsx 1> /dev/null 2>&1; then
                        mv redirect_results*.xlsx $OUTPUT_DIR/
                    else
                        echo "No XLSX file found"
                    fi
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Job completed"
        }
        failure {
            echo "❌ Job failed"
        }
    }
}
