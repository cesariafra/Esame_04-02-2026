class Artist:
    def __init__(self, artist_id, num_objects):
        self.artist_id = artist_id
        self.p = num_objects

    def __str__(self):
        return f"(ID: {self.artist_id}), {self.p}"

    def __repr__(self):
        return self.__str__()
