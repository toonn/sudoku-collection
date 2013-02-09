#! /usr/bin/env python
# This script collects sudoku puzzles from menneske.no

import urllib2
import re
import os
import sys

menneske = 'http://www.menneske.no/sudoku/eng/'
four_url = menneske + 'utskrift4.html'
top_url = menneske + 'top10.html'
category_url_part = menneske + 'random.html?diff='
number = menneske + 'showpuzzle.html?number='


def write_sudoku(sudoku):
    su = sudoku[2]
    sudoku_list = [[[su[i+j], su[i+j+1], su[i+j+2]] for j in xrange(0,9,3)]
                        for i in xrange(0,81,9)]
    sudoku_trips = [[' '.join(trip) for trip in row] for row in sudoku_list]
    sudoku_rows = ['    '.join(trips) for trips in sudoku_trips]
    sudoku_rows.insert(3, '')
    sudoku_rows.insert(7, '')
    sudoku_string = '\n'.join(sudoku_rows)
    with open('sudoku/{category}/{idnr}.sudoku'.format(idnr=sudoku[0], category=sudoku[1]),
                'w') as file:

        file.write(sudoku_string)

def parse_puzzle(html_source):
    sudoku_src = re.findall('<div class="grid"><table>.*?</table>', html_source,
                            flags=re.DOTALL)
    sudoku_nrs = [re.findall('[0-9]|&nbsp;', sud_src) for sud_src in sudoku_src]
    sudokus = [['.' if elem == '&nbsp;' else elem for elem in sud]
                    for sud in sudoku_nrs]
    
    return sudokus


def get_number(idnr):
    html = urllib2.urlopen(number + str(idnr)).read()
    category = re.findall('Difficulty: .*? \(', html)[0][12:-2]
    sudoku = (idnr, category, parse_puzzle(html)[0])

    return sudoku


def get_cat(category_nr):
    html = urllib2.urlopen(category_url_part + str(category_nr)).read()
    idnr = re.findall('number: [0-9]*?<', html)[0][8:-1]
    category = re.findall('Difficulty: .*? \(', html)[0][12:-2]
    sudoku = (idnr, category, parse_puzzle(html)[0])

    return sudoku


def get_four():
    html = urllib2.urlopen(four_url).read()
    idnrs = [idnr[6:-1] for idnr in re.findall('idnr: [0-9]*?<', html)]
    categories = [category[12:-2] for category in re.findall('Difficulty: .*? \(', html)]
    sudokus = zip(idnrs, categories, parse_puzzle(html))

    return sudokus


def get_top10():
    html = urllib2.urlopen(top_url).read()
    nrs = [nr[7:] for nr in re.findall('number=[0-9]*', html)]
    sudokus = [get_number(nr) for nr in nrs]

    return sudokus


def collect_with_getfour(number_of_times):
    for i in xrange(number_of_times):
        for sudoku in get_four():
            write_sudoku(sudoku)
    

if __name__ == '__main__':
    collect_with_getfour(sys.argv[1])
    nr_suds = [len(os.listdir(os.path.join('sudoku',d))) for d in os.listdir('sudoku')]
    print 'Max: {max}, Tot: {tot}'.format(max=max(nr_suds), tot=sum(nr_suds))

