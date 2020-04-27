import utils
import reader
r=reader.Reader('sample.mind.gz')
s=iter(r)
s0=next(s)
c=utils.Context()
from parsers.feelings import FeelingsParser
p=FeelingsParser()
p.parse(c,s0)
