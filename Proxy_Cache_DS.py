import collections
import os

class Node(object):
    def __init__(self, name, freq):
        self.name = name
        self.freq = freq
        self.next = None
        self.prev = None

    def getValue(self):
        return self.name


class LinkedList(object):
    def __init__(self):
        self.head = None
        self.tail = None
    
    def append(self, node):
        if self.head is None:
            self.head = node
        else:
            self.tail.next = node
            node.prev = self.tail
        self.tail = node
            
    def delete(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        del node

    def print_list(self):
        curr = self.head
        while curr is not None:
            print(curr.name)
            curr = curr.next



class LFUCache(object):

    def __init__(self, capacity):
        
        self.capa = capacity
        self.size = 0
        self.min_freq = 0
        self.freqList = collections.defaultdict(LinkedList)
        self.nameHash = {}


    def getItem(self, name):
        
        if name not in self.nameHash:
            return -1

        old_node = self.nameHash[name]
        self.nameHash[name] = Node(name, old_node.freq)
        self.freqList[old_node.freq].delete(old_node)
        if not self.freqList[self.nameHash[name].freq].head:
            del self.freqList[self.nameHash[name].freq]
            if self.min_freq == self.nameHash[name].freq:
                self.min_freq += 1

        self.nameHash[name].freq += 1
        self.freqList[self.nameHash[name].freq].append(self.nameHash[name])

        return self.nameHash[name].freq
        

    def insertItem(self, name):
        
        if self.capa <= 0:
            return

        if self.getItem(name) != -1:
            
            return
        
        if self.size == self.capa:
            # print("deleting")
            n = self.freqList[self.min_freq].head
            os.remove(n.name)
            del self.nameHash[self.freqList[self.min_freq].head.name]
            self.freqList[self.min_freq].delete(self.freqList[self.min_freq].head)
            if not self.freqList[self.min_freq].head:
                del self.freqList[self.min_freq]
            self.size -= 1

        self.min_freq = 1
        self.nameHash[name] = Node(name, self.min_freq)
        self.freqList[self.nameHash[name].freq].append(self.nameHash[name])
        self.size += 1

def print_cache(cache):
    for list_i in cache.freqList:
        print("\nCache Item with frequency ",list_i)
        print("-----------------------------------------------")
        cache.freqList[list_i].print_list()