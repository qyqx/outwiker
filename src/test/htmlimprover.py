#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.htmlimprover import HtmlImprover

class HtmlImproverTest (unittest.TestCase):
    def test1 (self):
        src = ur"""<h2>Attach links</h2><p>Attach:file.odt<br><a href="__attach/file.odt">file.odt</a><br><a href="__attach/file.odt">alternative text</a><br><a href="__attach/file with spaces.pdf">file with spaces.pdf</a><p><h2>Images</h2>"""

        expectedResult = ur"""
<h2>Attach links</h2></p>

<p>Attach:file.odt
<br><a href="__attach/file.odt">file.odt</a>
<br><a href="__attach/file.odt">alternative text</a>
<br><a href="__attach/file with spaces.pdf">file with spaces.pdf</a></p>

<p>
<h2>Images</h2>"""

        result = HtmlImprover.run (src)
        self.assertEqual (expectedResult, result)
    

    def test2 (self):
        src = ur"""<ul><li>Несортированный список. Элемент 1</li><li>Несортированный список. Элемент 2</li><li>Несортированный список. Элемент 3</li><ol><li>Вложенный сортированный список. Элемент 1</li><li>Вложенный сортированный список. Элемент 2</li><li>Вложенный сортированный список. Элемент 3</li><li>Вложенный сортированный список. Элемент 4</li><ul><li>Совсем вложенный сортированный список. Элемент 1</li><li>Совсем вложенный сортированный список. Элемент 2</li></ul><li>Вложенный сортированный список. Элемент 5</li></ol><ul><li>Вложенный несортированный список. Элемент 1</li></ul></ul>"""

        expectedResult = ur"""
<ul>
<li>Несортированный список. Элемент 1</li>
<li>Несортированный список. Элемент 2</li>
<li>Несортированный список. Элемент 3</li>
<ol>
<li>Вложенный сортированный список. Элемент 1</li>
<li>Вложенный сортированный список. Элемент 2</li>
<li>Вложенный сортированный список. Элемент 3</li>
<li>Вложенный сортированный список. Элемент 4</li>
<ul>
<li>Совсем вложенный сортированный список. Элемент 1</li>
<li>Совсем вложенный сортированный список. Элемент 2</li>
</ul>
<li>Вложенный сортированный список. Элемент 5</li>
</ol>
<ul>
<li>Вложенный несортированный список. Элемент 1</li>
</ul>
</ul>"""

        result = HtmlImprover.run (src)
        self.assertEqual (expectedResult, result, result)
    

    def test3 (self):
        src = ur"""qweqweqw qweqwe<br>qwewqeqwe wqe<p>qweqweqw qwe qweqwe<pre>
аап ываыв ываываыываы ыва ыва
ываыва выа выа

ываыв фывфв фывфывыф ыфв
вапвапввап вапвапвап

вапвапвап вапваапва</pre><p>sdfsdf sdfsdf<br>sdfsdf<br>sdf sdfsdf sdf"""

        expectedResult = ur"""qweqweqw qweqwe
<br>qwewqeqwe wqe</p>

<p>qweqweqw qwe qweqwe
<pre>
аап ываыв ываываыываы ыва ыва
ываыва выа выа

ываыв фывфв фывфывыф ыфв
вапвапввап вапвапвап

вапвапвап вапваапва</pre></p>

<p>sdfsdf sdfsdf
<br>sdfsdf
<br>sdf sdfsdf sdf"""

        result = HtmlImprover.run (src)
        self.assertEqual (expectedResult, result, result)
