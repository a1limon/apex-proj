import os
import sys
import logging
import requests
from typing import Any, Dict

class ApexLegendsAPI:
    HEADERS = {"Authorization": os.environ.get("APEX_API_KEY")}
    BASE_URL = "https://api.mozambiquehe.re/"

    def __init__(self, api_key: str, logger= None):
        self.api_key = api_key

        if logger is not None:
            self.log = logger
        else:
            log = logging.getLogger("apex_logger")
            stdout_handler = logging.StreamHandler(sys.stdout)
            log.addHandler(stdout_handler)
            self.log = log
    
    def request(self, path, params: Dict[str, any]) -> Dict[str, Any]:
        """_summary_

        Args:
            path (_type_): _description_
            params (Dict[str, any]): _description_

        Returns:
            Dict[str, Any]: _description_
        """

        response = requests.get(
            url=self.BASE_URL + path,
            headers=self.HEADERS,
            params={
                "api_key": self.api_key,
                **params
            },

        )

        if response.status_code == 429:
            self.log.warning(f"Rate limit reached for {path}")
        
        response.raise_for_status()
        return response.json()
    
    def get_player_stats(self, player, platform):
        path = f'bridge?auth={self.api_key}&player={player}&platform={platform}'
        return self.request(path, {})



if __name__ == "__main__":
    apex_obj =  ApexLegendsAPI(os.environ.get("APEX_API_KEY"))
    my_player = "Limown_"
    my_platform = "PS4"
    data = apex_obj.get_player_stats(player="girth_gorilla", platform="PS4")
    print(data)
