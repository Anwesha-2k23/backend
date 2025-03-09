from django.core.mail.backends.smtp import EmailBackend


class CustomEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False
        self.connection = self.connection_class(self.host, self.port, timeout=self.timeout)
        self.connection.ehlo()
        if self.use_tls:
            self.connection.starttls()  # Ensure no unsupported arguments are passed
            self.connection.ehlo()
        if self.username and self.password:
            self.connection.login(self.username, self.password)
        return True
