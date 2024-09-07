from datetime import datetime
from sqlalchemy import desc, or_

from Mylog import cache, app
from Mylog.store.iService import ServerBase
from Mylog.models import Cover
from Mylog.util.cos import COS
from Mylog.util.tool import short_uuid, validate_datetime

cos = COS(app.config['COS_URL'])
cos.production = True


class CoverService(ServerBase):
    def create(self, file, data: dict):
        saying = data.get('saying')
        time = data.get('date')
        time = datetime.now() if time is None else validate_datetime(time)
        if cos.post2one(file, file.filename):
            one = Cover(
                id=short_uuid(),
                url=cos.one_baseurl + file.filename,
                saying=saying,
                time=time,
            )
            self.save2db(one)
            self.update_cache()

    def get_all(self) -> list:
        ones = Cover.query.order_by(desc(Cover.time))[0:]
        return [self.extract_attr(one) for one in ones]

    def get_by_many(self, args: dict):
        page = args.get('page', 0)
        limit = args.get('limit', 10)
        keyword = args.get('keyword', '')
        query = Cover.query.filter(or_(Cover.saying.like(f'%{keyword}%'))).order_by(
            desc(Cover.time)
        )
        total = query.count()
        covers = query.offset(page * limit).limit(limit)
        return {'total': total, 'rows': [self.extract_attr(c) for c in covers]}

    def get_one(self, id: int):
        one = Cover.query.order_by(desc(Cover.time))[id]
        if one:
            return self.extract_attr(one)
        else:
            return None

    def update(self, data: dict) -> bool:
        id = data.get('id')
        one = Cover.query.filter(Cover.id == id).first()
        if one:
            for k in data.keys():
                try:
                    setattr(one, k, data[k])
                    self.save2db(one)
                except:
                    continue
            self.update_cache()

            return True

        else:
            raise ValueError('无记录')

    def cover(self, id, file) -> bool:
        one = Cover.query.filter(Cover.id == id).first()
        if cos.post2one(file, file.filename):
            one.url = cos.one_baseurl + file.filename
            self.save2db(one)
            self.update_cache()
            return True
        else:
            raise ValueError()

    def delete(self, id):
        one = Cover.query.filter(Cover.id == id).first()
        if one:
            self.delete_from_db(one)
            self.update_cache()

    def extract_attr(self, obj: object) -> dict:
        prop_dict = vars(obj)
        response_dict = {}
        for k, v in prop_dict.items():
            if k.startswith("_") or k.endswith("_"):
                continue
            if isinstance(v, datetime):
                response_dict['time'] = v.strftime('%Y-%m-%d')
                continue
            else:
                prop_v = v
            response_dict[k] = prop_v
        return response_dict

    def update_cache(self):
        cache.delete('moment')
