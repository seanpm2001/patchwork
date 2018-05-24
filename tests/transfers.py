from patchwork.transfers import rsync


base = "rsync  -pthrvz"
end = "localpath user@host:remotepath"


class transfers:

    class rsync_:

        def _expect(self, cxn, expected, kwargs=None):
            if kwargs is None:
                kwargs = {}
            rsync(cxn, "localpath", "remotepath", **kwargs)
            command = cxn.local.call_args[0][0]
            assert expected == command

        def base_case(self, cxn):
            expected = "{}  --rsh='ssh  -p 22 ' {}".format(base, end)
            self._expect(cxn, expected)

        def single_key_filename_honored(self, cxn):
            cxn.connect_kwargs.key_filename = "secret.key"
            expected = "{}  --rsh='ssh -i secret.key -p 22 ' {}".format(
                base, end
            )
            self._expect(cxn, expected)

        def multiple_key_filenames_honored(self, cxn):
            cxn.connect_kwargs.key_filename = ["secret1.key", "secret2.key"]
            keys = "-i secret1.key -i secret2.key"
            expected = "{}  --rsh='ssh {} -p 22 ' {}".format(base, keys, end)
            self._expect(cxn, expected)