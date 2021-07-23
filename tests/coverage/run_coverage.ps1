# Set running directory to project root directory
cd ..; cd ..;
# Run coverage
coverage run --source anchorage -m unittest discover;
# Generate badge
coverage-badge -o coverage.svg;
# Coverage destination
$CovDest = "tests\coverage";

# Remove previous .coverage and badge
$CovName = "$CovDest\.coverage";
$BadgeName = "$CovDest\coverage.svg";
if (Test-Path $CovName) {
  Remove-Item $CovName;
}
if (Test-Path $BadgeName) {
  Remove-Item $BadgeName;
}

# Move .coverage and badge to \coverage
Move-Item -Path ".coverage" -Destination $CovDest;
Move-Item -Path "coverage.svg" -Destination $CovDest;

coverage report;

cd tests; cd coverage;

docker stop $(docker ps -a -q);
docker container rm $(docker container ls -aq);
