# Use Windows Server Core as base image
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Use PowerShell for all shell commands
SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

# Environment variables
ENV PYTHONIOENCODING UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHON_VERSION 3.13.5
ENV PYTHON_SHA256 c1cb40978b28f696b111c36034a1bdeda17d25e35c74a08ef5e5ff405a63fc20

# Install Python
RUN $url = ('https://www.python.org/ftp/python/{0}/python-{1}-amd64.exe' -f ($env:PYTHON_VERSION -replace '[a-z]+[0-9]*$', ''), $env:PYTHON_VERSION); \
    Write-Host ('Downloading {0} ...' -f $url); \
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
    Invoke-WebRequest -Uri $url -OutFile 'python-installer.exe'; \
    \
    Write-Host ('Verifying sha256 ({0}) ...' -f $env:PYTHON_SHA256); \
    if ((Get-FileHash python-installer.exe -Algorithm sha256).Hash -ne $env:PYTHON_SHA256) { \
        Write-Host 'SHA256 check FAILED!'; exit 1; \
    }; \
    \
    Write-Host 'Installing Python ...'; \
    $exitCode = (Start-Process python-installer.exe -Wait -NoNewWindow -PassThru \
        -ArgumentList @( \
            '/quiet', \
            'InstallAllUsers=1', \
            'TargetDir=C:\Python', \
            'PrependPath=1', \
            'Shortcuts=0', \
            'Include_doc=0', \
            'Include_pip=1', \
            'Include_test=0' \
        ) \
    ).ExitCode; \
    if ($exitCode -ne 0) { \
        Write-Host 'Python installer failed with exit code:' $exitCode; exit $exitCode; \
    }; \
    \
    Remove-Item python-installer.exe -Force; \
    $env:PATH = [Environment]::GetEnvironmentVariable('PATH', [EnvironmentVariableTarget]::Machine); \
    pip --version; \
    python --version

# Set working directory inside container
WORKDIR C:/app

# Copy Django project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose Django dev server port
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
