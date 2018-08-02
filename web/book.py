from flask import jsonify, request, current_app, flash, render_template
from sqlalchemy.dialects.mysql import json

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key

from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from . import web


# @web.route('/book/search/<q>/<page>')
@web.route('/book/search')
def search():
    """
        q :普通关键字 （keyword) isbn
        page
    """
    # 第一种方式 验证方法q,page
    # q = request.args['q']
    # page = request.args['page']
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()     # strip()除去q前后存在空格
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
            # result = YuShuBook.search_by_isbn(q)
            # result = BookViewModel.package_single(result, q)
        else:
            yushu_book.search_by_keyword(q, page)
            # result = YuShuBook.search_by_keyword(q, page)
            # result = BookViewModel.package_collection(result, q)

        books.fill(yushu_book, q)
        return json.dumps(books, default=lambda o: o.__dict__)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books, form=form)
    # return json.dumps(result), 200, {'content-type': 'application/json'}


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)
    return render_template('book_detail_html', book=book, wishes=[], gifts=[])

