from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import (ProviderAccount,
                                                  AuthAction)
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.app_settings import QUERY_EMAIL


class Scope(object):
    EMAIL = 'email'
    PROFILE = 'profile'


class SurveyMonkeyOAuth2Account(ProviderAccount):
    def to_str(self):
        dflt = super(SurveyMonkeyOAuth2Account, self).to_str()
        return self.account.extra_data.get('first_name', dflt) + ' ' + self.account.extra_data.get('last_name', dflt)


class SurveyMonkey2Provider(OAuth2Provider):
    id = 'surveymonkey'
    name = 'SurveyMonkey'
    account_class = SurveyMonkeyOAuth2Account

    def get_default_scope(self):
        scope = [Scope.PROFILE]
        if QUERY_EMAIL:
            scope.append(Scope.EMAIL)
        return scope

    def get_auth_params(self, request, action):
        ret = super(SurveyMonkey2Provider, self).get_auth_params(request, action)
        if action == AuthAction.REAUTHENTICATE:
            ret['prompt'] = 'select_account'
        return ret

    def extract_uid(self, data):
        return data["id"]  # str() ?

    def extract_common_fields(self, data):
        return dict(email=data.get('email'),
                    last_name=data.get('last_name'),
                    first_name=data.get('first_name'))

        # def extract_email_addresses(self, data):
        #     ret = []
        #     email = data.get('email')
        #     if email and data.get('verified_email'):
        #         ret.append(EmailAddress(email=email,
        #                    verified=True,
        #                    primary=True))
        #     return ret


providers.registry.register(SurveyMonkey2Provider)
