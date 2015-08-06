# Copyright (c) 2004-2005 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""Text formatting drivers for ureports"""

__revision__ = "$Id: text_writer.py,v 1.9 2005-11-22 13:13:13 syt Exp $"

from os import linesep

from clonedigger.logilab.common.ureports import BaseWriter

TITLE_UNDERLINES = ['', '=', '-', '`', '.', '~', '^']
BULLETS = ['*', '-']
 
class TextWriter(BaseWriter):
    """format layouts as text
    (ReStructured inspiration but not totally handled yet)
    """
    def begin_format(self, layout):
        super(TextWriter, self).begin_format(layout)
        self.list_level = 0
        self.pending_urls = []
        
    def visit_section(self, layout):
        """display a section as text
        """
        self.section += 1
        self.writeln()
        self.format_children(layout)
        if self.pending_urls:
            self.writeln()
            for label, url in self.pending_urls:
                self.writeln('.. _`%s`: %s' % (label, url))
            self.pending_urls = []
        self.section -= 1
        self.writeln()
            
    def visit_title(self, layout):
        title = ''.join(list(self.compute_content(layout)))
        self.writeln(title)
        try:
            self.writeln(TITLE_UNDERLINES[self.section] * len(title))
        except IndexError:
            print "FIXME TITLE TOO DEEP. TURNING TITLE INTO TEXT"
        
    def visit_paragraph(self, layout):
        """enter a paragraph"""
        self.format_children(layout)
        self.writeln()
         
    def visit_span(self, layout):
        """enter a span"""
        self.format_children(layout)
         
    def visit_table(self, layout):
        """display a table as text"""
        table_content = self.get_table_content(layout)
        # get columns width
        cols_width = [0]*len(table_content[0])
        for row in table_content:
            for index in range(len(row)):
                col = row[index]
                cols_width[index] = max(cols_width[index], len(col))
        if layout.klass == 'field':
            self.field_table(layout, table_content, cols_width)
        else:
            self.default_table(layout, table_content, cols_width)
        self.writeln()
        
    def default_table(self, layout, table_content, cols_width):
        """format a table"""
        cols_width = [size+1 for size in cols_width]
        format_strings = ' '.join(['%%-%ss'] * len(cols_width))
        format_strings = format_strings % tuple(cols_width)
        format_strings = format_strings.split(' ')
        table_linesep = '\n+' + '+'.join(['-'*w for w in cols_width]) + '+\n'
        headsep = '\n+' + '+'.join(['='*w for w in cols_width]) + '+\n'
        # FIXME: layout.cheaders
        self.write(table_linesep)
        for i in range(len(table_content)):
            self.write('|')
            line = table_content[i]
            for j in range(len(line)):
                self.write(format_strings[j] % line[j])
                self.write('|')
            if i == 0 and layout.rheaders:
                self.write(headsep)
            else:
                self.write(table_linesep)
 
    def field_table(self, layout, table_content, cols_width):
        """special case for field table"""
        assert layout.cols == 2
        format_string = '%s%%-%ss: %%s' % (linesep, cols_width[0])
        for field, value in table_content:
            self.write(format_string % (field, value))
 

    def visit_list(self, layout):
        """display a list layout as text"""
        bullet = BULLETS[self.list_level % len(BULLETS)]
        indent = '  ' * self.list_level
        self.list_level += 1
        for child in layout.children:
            self.write('%s%s%s ' % (linesep, indent, bullet))
            child.accept(self)
        self.list_level -= 1

    def visit_link(self, layout):
        """add a hyperlink"""
        if layout.label != layout.url:
            self.write('`%s`_' % layout.label)
            self.pending_urls.append( (layout.label, layout.url) )
        else:
            self.write(layout.url)
            
    def visit_verbatimtext(self, layout):
        """display a verbatim layout as text (so difficult ;)
        """
        self.writeln('::\n')
        for line in layout.data.splitlines():
            self.writeln('    ' + line)
        self.writeln()
        
    def visit_text(self, layout):
        """add some text"""
        self.write(layout.data)
            

