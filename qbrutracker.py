#VERSION: 1.0
#AUTHORS: alvin <alvin1979@mail.ru>
"""
	Copyright (C) 2016 alvin <alvin1979@mail.ru>
	
	This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""



import os
import io
import sys

import novaprinter

import urllib.parse

import tarfile
import shutil
  
cols		= ( "id", "category", "tor_id", "hash", "name", "size", "date" )
subfolder	= "rutracker-torrents"
trak_file_n	= "tracker.txt"
tracker_info_lnk	= "https://rutracker.org/forum/viewtopic.php?t="
limit		= 50
pack_cmd 	= "QB_PACK"
arch_ext	= ".tar.bz2"


files = [ 	"category_1.csv", 
			"category_2.csv", 
			"category_4.csv",
			"category_8.csv",
			"category_9.csv",
			"category_10.csv",
			"category_11.csv",
			"category_18.csv",
			"category_19.csv",
			"category_20.csv",
			"category_22.csv",
			"category_23.csv",
			"category_24.csv",
			"category_25.csv",
			"category_26.csv",
			"category_27.csv",
			"category_28.csv",
			"category_29.csv",
			"category_31.csv",
			"category_33.csv",
			"category_34.csv",
			"category_35.csv",
			"category_36.csv", 
			
			]



class qbrutracker :
	url						= "rutracker.org"
	name 					= "Offline Database of Rutracker.org"
	supported_categories 	= { 	
					"all" 		: files, 
					"movies" 	: [ files[ 1 ] ], 
					"tv" 		: [ files[ 2 ], files[ 7 ] ], 
					"music" 	: [ files[ 3 ], files[ 11 ], files[ 21 ], files[ 10 ], files[ 18 ] ], 
					"games" 	: [ files[ 8 ] ], 
					"software" 	: [ files[ 14 ], files[ 4 ] ], 
					"books" 	: [ files[ 19 ], files[ 13 ] ] 
				}
	archive = None
			
	def search( self, what, cat = "all" ) :
		results = []
		
		try :
			self.archive = tarfile.open( get_arch_path(), "r:bz2" )
		except :
			pass
			
		what = parse_request( what )		
		if not what :
			return
		
		for name in self.supported_categories[ cat ] :
			try :
				with get_latest_db( name, self.archive ) as db :
					results += search_db( db, what, len( cols ), len( results ) )
			except :
				pass
			
		for parsed in parse_results( results, load_trackers( self.archive ) ) :
			novaprinter.prettyPrinter( parsed )

			
	def __del__( self ) :
		if self.archive :
			self.archive.close()

def get_arch_path() :
	return ( get_data_dir() + arch_ext )
	
def pack_db() :
	new_arch = get_arch_path()
		
	with tarfile.open( new_arch, "w:bz2" ) as arch :
		data_dir 	= get_data_dir()
		latest 		= get_latest_db_dir( data_dir )
		if latest :
			arch.add( latest, filter = filter_ti )
			try :
				arch.add( os.path.join( get_data_dir(), trak_file_n ), filter = filter_ti )
			except :
				pass
			shutil.rmtree( data_dir, True )
	
def filter_ti( ti ) :
	ti.name = os.path.split( ti.name )[ 1 ]
	return ti
	
def get_latest_db_dir( db_dir ) :
	dirs = []
	
	for root, sub, files in os.walk( db_dir ) :
		dirs = [ os.path.join( root, dir ) for dir in sub ]
		break
	
	if dirs :
		return sorted( dirs, reverse = True )[ 0 ]
		
def get_latest_db( name, arch )	:
	if arch :
		return open_data( name, arch )
		
	latest = os.path.join( get_latest_db_dir( get_data_dir() ), name )
	
	return open( latest, encoding = "utf-8" )
			
def open_data( name, arch ) :
	encod = "utf-8"
	
	if not arch :	
		return open( os.path.join( get_data_dir(), name ), encoding = encod, errors = "ignore" )
	
	return io.TextIOWrapper( arch.extractfile( name ), encod )
			
def get_data_dir() :
	return os.path.join( get_up_dir( 3, __file__ ), subfolder )

def get_up_dir( lvl, path ) :
	for l in range( lvl ) :
		path = os.path.split( path )[ 0 ]
	print( path )
	return path	
	
def parse_results( res, trackers ) :
	ret = []

	for item in res :
		size = item[ cols.index( "size" ) ]
		name = "{} [ {} ]".format( item[ cols.index( "name" ) ], item[ cols.index( "category" ) ] )
		link 		= make_magnet( item[ cols.index( "hash" ) ], name, trackers )
		desc_link 	= make_info_lnk( item[ cols.index( "tor_id" ) ] )
	
		ignored = ""
		ret.append( { 	"link" : link, 
						"name" : name, 
						"size" : size, 
						"engine_url" : qbrutracker.url, 
						"seeds" : ignored, 
						"leech" : ignored, 
						"desc_link" : desc_link 
					} )	
	return ret				

def load_trackers( arch ) :
	trackers = []
	
	try :
		with open_data( trak_file_n, arch ) as traks :
			trackers = traks.read().split( "\n" )		
	except :
		pass

	return trackers	
	
def make_info_lnk( torrent_id ) :
	return tracker_info_lnk + str( torrent_id )

def parse_request( req ) :
	"""
	>>> parse_request( "-exclude%20=599%20include" )
	(['include'], ['exclude'], 599)
	"""
	
	req 	= urllib.parse.unquote( req )
	include = []
	exclude = []
	usr_lim = limit
	
	for word in req.split() :
		if len( word ) < 1 :
			continue
		if word[ 0 ] == "-" :
			exclude.append( word[ 1 : ] )
		elif word[ 0 ] == "=" :
			try :
				usr_lim = int( word[ 1 : ] )
			except ValueError :
				continue
		elif word == pack_cmd :
			pack_db()
			return
		else :
			include.append( word )
			
	return include, exclude, usr_lim

def search_db( file, what, expect, pre_num ) :	
	""" 
	Searches words line by line in file, split them and check result with expect, excludes words that start with "-" symbol.
	
	>>> global cols 
	>>> cols = ( '' )
	>>> file = io.StringIO( "torrent name first\\ntorrent name first second\\ntorrent name third" )
	>>> search_db( file, ( "first", "second", 6 ), 1, 5 )
	[['torrent name first']]
	"""	
	
	include, exclude, usr_lim = what
	out = []
	
	for line in file :
		if filter( include, line ) and not filter( exclude, line, False ) :
			parsed = parse_row( line, expect )
			if parsed :
				if usr_lim and not ( ( len( out ) + pre_num ) < usr_lim ) :	
					break
				out.append( parsed )

		
	return out
	
def parse_row( line, expect ) :
	""" 
	>>> parse_row( "\\"first\\";\\"second", 2 )
	['first', 'second']
	"""	
	
	item = line.strip().split( "\";\"" )
	item = [ i.replace( "\"", "" ) for i in item ]

	if len( item ) == expect :
		return item
	
def make_magnet( hash, name, trackers = [] ) :
	"""
	>>> make_magnet( "329841348432213464", "torrent name", ["http://tracker1", "udp://tracker2"] )
	'magnet:?xt=urn:btih:329841348432213464&dn=torrent%20name&tr=http%3A//tracker1&tr=udp%3A//tracker2&'
	"""
	args = [ ( "magnet:?xt=urn:btih:", hash ), ( "dn=", name ) ]
	
	for trak in trackers :
		args.append( ( "tr=", trak ) )
	
	link = ""
	
	for param, value in args :
		link += ( param + urllib.parse.quote( value ) + "&" )
	
	return link	

def filter( words, from_string, defu = True ) :
	"""
	>>> filter( ["word1", "Word2"], "There is no such word1 WORD2" )
	True
	"""
	
	if not len( words ) :
		return defu
		
	ret = True
	for word in words :
		ret = ret & ( word.lower() in from_string.lower() )
			
	return ret