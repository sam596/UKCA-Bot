from datetime import date


class WCA_API:
    url = "http://www.worldcubeassociation.org/api/v0/"
    # usage e.g. WCA_API().persons("2015SPEN01") returns "http://www.worldcubeassociation.org/api/v0/persons/2015SPEN01
    def persons(self, query):
        return self.url + "persons/" + query
    def upcoming(self, iso2):
        return self.url + "competitions?country_iso2=" + iso2 + "&start=" + date.today().isoformat()
    def recordslookup(self):
        return self.url + "records/"
