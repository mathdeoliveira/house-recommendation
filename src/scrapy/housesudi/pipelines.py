# -*- coding: utf-8 -*-
import sqlite3

## ZAP IMOVEIS
class ImoveisSqlitePipeline(object):
    def process_item(self, item, spider):
        self.conn.execute(
            'insert into udi_imoveis (preco, endereco, area, quartos, garagem, banheiros) values (:preco, :endereco, :area, :quartos, :garagem, :banheiros)',
            item
        )
        self.conn.commit()
        return item

    def create_table(self):
        result = self.conn.execute(
            'select name from sqlite_master where type = "table" and name = "udi_imoveis"'
        )
        try:
            _ = next(result)
        except StopIteration as _:
            self.conn.execute(
                'create table udi_imoveis (id integer primary key, preco varchar(30), endereco varchar(100), area varchar(50), quartos varchar(50), garagem varchar(50), banheiros varchar(50))'
            )

    def open_spider(self, spider):
        self.conn = sqlite3.connect('/home/matheus/Documentos/house-recommendation/data/db_udi_imoveis.sqlite3')
        self.create_table()

    def close_spider(self, spider):
        self.conn.close()
