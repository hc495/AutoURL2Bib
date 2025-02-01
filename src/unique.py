class collision_detection():
    def __init__(self, library):
        self.hash_table = {}
        for i in range(len(library.entries)):
            paper = library.entries[i]
            key = self.get_key(paper)
            if key in self.hash_table:
                self.hash_table[key].append(i)
            else:
                self.hash_table[key] = [i]
    
    def get_key(self, paper):
        key = paper['title'].lower()
        return key
    
    def detect_collision(self, paper):
        key = self.get_key(paper)
        if key in self.hash_table:
            return self.hash_table[key]
        else:
            return []
        
def collision_handle(paper1, paper2):
    if paper1['ID'] == paper2['ID']:
        return True
    elif "year" in paper1 and "year" in paper2:
        if int(paper1['year']) > int(paper2['year']):
            return True
        else:
            return False
    elif "year" in paper1:
        return True
    elif "year" in paper2:
        return False
    else:
        return True
    
def unique(library):
    collision = collision_detection(library)
    replace_table = []
    popset = set()
    popmap = {}
    for i in range(len(library.entries)):
        if i in popset:
            continue
        paper = library.entries[i]
        collision_list = collision.detect_collision(paper)
        if len(collision_list) > 1:
            for j in collision_list:
                if i == j:
                    continue
                if j in popset:
                    continue
                if collision_handle(paper, library.entries[j]):
                    popset.add(j)
                    popmap[j] = i
                    print(f"Collision detected: {paper['ID']} and {library.entries[j]['ID']}, {paper['title']}. Remain {paper['ID']}.")
                else:
                    popset.add(i)
                    popmap[i] = j
                    print(f"Collision detected: {paper['ID']} and {library.entries[j]['ID']}, {paper['title']}. Remain {library.entries[j]['ID']}.")
    for k, v in popmap.items():
        if library.entries[k]['ID'] != library.entries[v]['ID']:
            replace_table.append("Replace " + library.entries[k]['ID'] + " to " + library.entries[v]['ID'])
    for i in range(len(library.entries), -1, -1):
        if i in popset:
            library.entries.pop(i)
    repeated_number = len(popset)
    return library, repeated_number, replace_table