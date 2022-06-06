import bz2
import time
import pickle
import requests
import threading
from bs4 import BeautifulSoup

class ApexPlayerScraper:
    HEADERS = {"Accept": "application/json"}
    BASE_URL = "https://apexlegendsstatus.com/stats/"
    
    def request(self):
        """_summary_

        Args:
            path (_type_): _description_
            params (Dict[str, any]): _description_

        Returns:
            Dict[str, Any]: _description_
        """

        try:
            response = requests.get(
                url=self.BASE_URL,
                headers=self.HEADERS,
            )

            if response.status_code == 429:
                self.log.warning(f"Rate limit reached")
        
            response.raise_for_status()
        
        except requests.logging.exceptions.HTTPError as error:
            print(error)

        
        return response
    
    def scrape_player_names(self):
        response = self.request()
        soup = BeautifulSoup(response.content, 'lxml')
        players = soup.find_all("h2", attrs={"class":"profile-legend__name"})
        return players[0].text, players[1].text
    
    def scrape_n_player_names(self, n):
        maxthreads = 8
        ApexThread.player_names = list()
        at_list = list()
        for i in range(0, n, maxthreads):
            print(f'downloaded {i}/{n} apex player names...')
            for j in range(i, min(i+maxthreads, n)):
                at_list.append(ApexThread())
                at_list[len(at_list)-1].start()
            for j in range(i, min(i+maxthreads,n)):
                at_list[j].join()
        
        return ApexThread.player_names

    
class ApexThread(threading.Thread):
    player_names = list()
    lock = threading.Lock()

    def run(self):
        scraper = ApexPlayerScraper()
        player1, player2 = scraper.scrape_player_names()
        ApexThread.lock.acquire()
        ApexThread.player_names.append(player1)
        ApexThread.player_names.append(player2)
        ApexThread.lock.release()     

if __name__ == "__main__":
    t0 = time.time()

    #Load old data
    try:
        with bz2.BZ2File('apex_players.bz2', 'rb') as f:  #Use datacompression BZ2
            data = pickle.load(f)
            print(f'current num of player names: {len(data)}')
    except:
        data = []
       

    player_names = ApexPlayerScraper().scrape_n_player_names(1000)

    newdata = player_names
    print(f"new players scraped: {len(list(set(data+newdata))) - len(data)}")
    
    t1 = time.time()
    print(('took %f' % (t1 - t0)))
    
    #Save new data   
    with bz2.BZ2File('apex_players.bz2', 'wb') as f: #Use datacompression BZ2
        pickle.dump(list(set(data+newdata)), f)
    