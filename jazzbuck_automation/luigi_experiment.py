import luigi


class PocketDownload(luigi.Task):
    """ """

    dt = luigi.DateMinuteParameter(interval=5)

    def requires(self):
        return {
            "last_download": PocketDownload(self.dt - datetime.timedelta(minutes=10)),
            "secrets": SecretsLoad(),
        }

    def run(self):
        with open(self.input()["secrets"], "r") as r:
            secrets = yaml.safe_load(r)
        pocket = PocketSession(
            username=secrets["pocket"]["username"],
            consumer_key=secrets["pocket"]["consumer_key"],
            access_token=secrets["pocket"]["access_token"],
        )
        pass


class SecretsLoad(luigi.ExternalTask):
    """ """

    secrets = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(secrets)


class DateLastPocketAccess(luigi.Task):
    """ """

    date = luigi.DateParameter()

    def output(self):
        return luigi.LocalTarget("last_pocket_access.txt")


class SendPocketData(luigi.Task):
    """ """

    pass
