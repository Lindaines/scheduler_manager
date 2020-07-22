import subprocess
import os

from logzero import logger

import settings


def configuration(app):
    @app.cli.group()
    def commands():
        """Useful commands like lint, tests and complexity"""

    @commands.command("lint")
    def lint():
        """Run Lint to arrange code according to PEP8"""
        _lint()

    @commands.command("coverage")
    def coverage():
        """Performs coverage tests"""
        _coverage()

    @commands.command("coverage-server")
    def coverage_server():
        """Start server to view tested files"""
        try:
            _coverage()
            _coverage_server()
        except KeyboardInterrupt:
            logger.info("Command canceled")

    @commands.command("complexity")
    def complexity():
        """Calculate the complexity of project methods"""
        _complexity()

    @commands.command("all")
    def all():
        """Runs Lint, complexity, and tests commands"""
        _lint()
        _complexity()
        _coverage()

    def _lint():
        try:
            logger.info("Running pre-commit...")
            subprocess.run(["pre-commit", "install"])
            subprocess.run(["pre-commit", "run", "--all-files"])
        except KeyboardInterrupt:
            logger.info("Command canceled")

    def _coverage():
        try:
            logger.info("Running tests...")
            subprocess.run(["coverage", "run", "-m", "unittest", "discover", "tests"])
            subprocess.run(["coverage", "report"])
        except KeyboardInterrupt:
            logger.info("Command canceled")

    def _complexity():
        try:
            logger.info("Calculating complexity...")
            subprocess.run(
                [
                    "radon",
                    "cc",
                    "-s",
                    "-a",
                    "-nb",
                    "--total-average",
                    "-e",
                    "venv*",
                    ".",
                ]
            )
        except KeyboardInterrupt:
            logger.info("Command canceled")

    def _coverage_server():
        logger.info("Generating files...")
        subprocess.run(["coverage", "html"])
        os.chdir(settings.basedir + "/htmlcov")
        subprocess.run(["python", "-m", "http.server"])
