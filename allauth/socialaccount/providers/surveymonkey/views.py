from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
import requests

from .provider import SurveyMonkey2Provider


class SurveyMonkey2Adapter(OAuth2Adapter):
    provider_id = SurveyMonkey2Provider.id
    access_token_url = "https://api.surveymonkey.net/oauth/token"
    authorize_url = "https://api.surveymonkey.net/oauth/authorize"
    profile_url = "https://api.surveymonkey.net/v2/user"
    # profile_url = "https://api.surveymonkey.net/v2/user/get_user_details"
    redirect_uri_protocol = 'http'  # or https?

    def complete_login(self, request, app, token, **kwargs):

        extra_data = requests.get(self.profile_url, params={
            'access_token': token.token
        })

        # This only here because of weird response from the test suite
        if isinstance(extra_data, list):
            extra_data = extra_data[0]

        return self.get_provider().sociallogin_from_response(
            request,
            extra_data.json()
        )


oauth_login = OAuth2LoginView.adapter_view(SurveyMonkey2Adapter)
oauth_callback = OAuth2CallbackView.adapter_view(SurveyMonkey2Adapter)
