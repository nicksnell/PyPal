#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PyPal setup script

from setuptools import setup, find_packages

long_description = """PayPal API interface

Python interface to the PayPal Web Payments Pro API.

Currently only supports NVP interactions and a small 
subset of the API. More to come....
"""

setup(
	name='PyPal',
	version=0.1,
	description='PayPal API interface',
	long_description=long_description,
	author='Nick Snell',
	author_email='nick@orpo.co.uk',
	url='http://orpo.co.uk/code/',
	download_url='',
	license='BSD',
	platforms=[],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'License :: OSI Approved :: BSD License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	],
	zip_safe=True,
	packages=find_packages(exclude=['tests',]),
	dependency_links = [
	
	],
	entry_points = {
	
	},
	install_requires=[
	
	]
)