# here RAs are h:m:s.ss but can be degrees
# (this assume fk5, if you want to use
# galactic coords we have to change some
# things)
ras = ['3:43:27.94', '3:43:33.44','3:43:22.44','3:43:29.04','3:43:23.54',
	'3:42:58.24','3:44:35.04','3:43:32.34','3:43:26.84',
	'3:44:26.20','3:42:20.77','3:42:24.13','3:44:31.83']
# here DECs are d:m:s.ss but can be degrees
# (this assume fk5, if you want to use
# galactic coords we have to change some
# things)

decs = ['-30:00:27.5', '-30:00:57.1','-29:59:57.9','-30:01:34.0','-30:01:04.4',
	'-29:55:46.1','-29:57:22.3','-29:59:50.6','-29:59:21.0','-29:53:33.4',
	'-30:03:30.6','-29:56:44.2','-30:04:08.9']

# Widths of your ellipses in arcsec
widths = [29.86069718374397297, 29.86069718374397297,29.86069718374397297,29.86069718374397297,29.86069718374397297,
29.86069718374397297,29.86069718374397297,29.86069718374397297,29.86069718374397297,29.86069718374397297,
29.86069718374397297,29.86069718374397297,29.86069718374397297]

# Heights of your ellipses in arcsec
heights = [41.0172274967990944,41.0172274967990944,41.0172274967990944,41.0172274967990944,41.0172274967990944,41.0172274967990944,41.0172274967990944,41.0172274967990944,41.0172274967990944,41.0172274967990944,41.0172274967990944,41.0172274967990944,41.0172274967990944]

# Position angle of your ellipses in degrees
pas = [68.2081243317, 68.2081243317,68.2081243317,68.2081243317,68.2081243317,68.2081243317,68.2081243317,68.2081243317,68.2081243317,68.2081243317,68.2081243317,68.2081243317,68.2081243317]

# Header for the reg file
header = ['# Region file format: DS9 version 4.1',
          ('global color=blue dashlist=8 3 '
           'width=2 font="helvetica 10 '
           'normal roman" select=1 highlite=1 '
           'dash=0 fixed=0 edit=1 move=1 '
           'delete=1 include=1 source=1'),
          'fk5']

# Make your ellipses
for r, ra in enumerate(ras):
    line = ('ellipse({0},{1},{2}",{3}",{4})').format(ra,
                                                     decs[r],
                                                     widths[r],
                                                     heights[r],
                                                     pas[r])
    header.append(line)

# Write everything into a file
with open(('regionfile.reg'), 'w') as filehandle:
    for listitem in header:
        filehandle.write('{}\n'.format(listitem))
