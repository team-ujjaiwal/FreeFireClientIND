# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: a.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x07\x61.proto\x12\x05proto\"\xc2\x02\n\x1a\x43SGetPlayerPersonalShowRes\x12\"\n\x07players\x18\x01 \x03(\x0b\x32\x11.proto.PlayerInfo\x12#\n\tinventory\x18\x02 \x01(\x0b\x32\x10.proto.Inventory\x12\x1d\n\x04\x63lan\x18\x06 \x01(\x0b\x32\x0f.proto.ClanInfo\x12#\n\x08teammate\x18\x07 \x01(\x0b\x32\x11.proto.PlayerInfo\x12\'\n\x0b\x61\x63hievement\x18\x08 \x01(\x0b\x32\x12.proto.Achievement\x12#\n\x06status\x18\t \x01(\x0b\x32\x13.proto.PlayerStatus\x12!\n\x08\x63urrency\x18\n \x01(\x0b\x32\x0f.proto.Currency\x12&\n\x05\x65vent\x18\x0b \x01(\x0b\x32\x17.proto.TimeLimitedEvent\"\xe3\x05\n\nPlayerInfo\x12\x0f\n\x07user_id\x18\x01 \x01(\x03\x12\x14\n\x0c\x61\x63\x63ount_type\x18\x02 \x01(\x05\x12\x10\n\x08username\x18\x03 \x01(\t\x12\x14\n\x0c\x63ountry_code\x18\x05 \x01(\t\x12\x0b\n\x03\x61ge\x18\x06 \x01(\x05\x12\r\n\x05level\x18\x07 \x01(\x05\x12\x0e\n\x06\x62\x61nner\x18\x0b \x01(\x03\x12\x0e\n\x06\x61vatar\x18\x0c \x01(\x03\x12\x0c\n\x04rank\x18\x0e \x01(\x05\x12\x19\n\x11\x65xperience_points\x18\x0f \x01(\x05\x12\x18\n\x10unknown_field_17\x18\x11 \x01(\x05\x12\x16\n\x0ematches_played\x18\x12 \x01(\x05\x12\x19\n\x11unique_identifier\x18\x13 \x01(\x06\x12\x14\n\x0c\x63ombat_skill\x18\x14 \x01(\x05\x12\x13\n\x0btotal_kills\x18\x15 \x01(\x05\x12\x12\n\nlast_login\x18\x18 \x01(\x03\x12\x0e\n\x06health\x18\x1e \x01(\x05\x12\x0f\n\x07stamina\x18\x1f \x01(\x05\x12\x16\n\x0e\x65ncrypted_data\x18  \x01(\x0c\x12\x14\n\x0c\x63urrent_rank\x18# \x01(\x05\x12\x12\n\nmax_health\x18$ \x01(\x05\x12 \n\x08\x63lan_tag\x18) \x01(\x0b\x32\x0e.proto.ClanTag\x12\x16\n\x0e\x63lan_join_date\x18, \x01(\x03\x12\x18\n\x10unknown_field_48\x18\x30 \x01(\x05\x12\'\n\x07premium\x18\x31 \x01(\x0b\x32\x16.proto.PremiumFeatures\x12\x14\n\x0cgame_version\x18\x32 \x01(\t\x12\x11\n\tis_online\x18\x34 \x01(\x08\x12\x10\n\x08in_match\x18\x35 \x01(\x08\x12\x1f\n\x05stats\x18= \x03(\x0b\x32\x10.proto.StatEntry\x12\'\n\x08\x61\x63tivity\x18? \x01(\x0b\x32\x15.proto.RecentActivity\x12\x30\n\x10status_indicator\x18@ \x01(\x0b\x32\x16.proto.StatusIndicator\"J\n\x07\x43lanTag\x12\x11\n\ttag_bytes\x18\x04 \x01(\x0c\x12\x13\n\x0btag_display\x18\x05 \x01(\t\x12\x17\n\x0funknown_field_7\x18\x07 \x01(\x05\">\n\x0fPremiumFeatures\x12\x15\n\rpremium_level\x18\x02 \x01(\x05\x12\x14\n\x0cpremium_days\x18\x03 \x01(\x05\"N\n\tStatEntry\x12\x0f\n\x07stat_id\x18\x01 \x01(\x05\x12\x0c\n\x04tier\x18\x02 \x01(\x05\x12\"\n\x07\x64\x65tails\x18\x03 \x01(\x0b\x32\x11.proto.StatDetail\"h\n\nStatDetail\x12\x11\n\tstat_type\x18\x01 \x01(\x05\x12\x10\n\x08progress\x18\x02 \x01(\x05\x12\x11\n\tmax_value\x18\x03 \x01(\x05\x12\x0f\n\x07unlocks\x18\x04 \x01(\x05\x12\x11\n\tcompleted\x18\x05 \x01(\x08\"7\n\x0eRecentActivity\x12%\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\x14.proto.ActivityEntry\"H\n\rActivityEntry\x12\x15\n\ractivity_type\x18\x01 \x01(\x05\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x12\r\n\x05\x63ount\x18\x03 \x01(\x05\"<\n\x0fStatusIndicator\x12\x13\n\x0bstatus_type\x18\x01 \x01(\x05\x12\x14\n\x0cstatus_value\x18\x02 \x01(\x05\"\xc5\x01\n\tInventory\x12\x14\n\x0cinventory_id\x18\x01 \x01(\x05\x12\x10\n\x08\x63\x61pacity\x18\x03 \x01(\x05\x12\x16\n\x0einventory_hash\x18\x04 \x01(\x0c\x12#\n\x05items\x18\x05 \x03(\x0b\x32\x14.proto.InventoryItem\x12\x0f\n\x07version\x18\x06 \x01(\x05\x12\x13\n\x0bis_equipped\x18\x08 \x01(\x08\x12\x13\n\x0blast_update\x18\x0b \x01(\x03\x12\x18\n\x10unknown_field_12\x18\x0c \x01(\x05\"f\n\rInventoryItem\x12\x14\n\nconsumable\x18\x01 \x01(\x05H\x00\x12\x10\n\x06weapon\x18\x02 \x01(\x05H\x00\x12\x0e\n\x04skin\x18\x03 \x01(\x05H\x00\x12\x10\n\x08quantity\x18\x04 \x01(\x05\x42\x0b\n\titem_type\"\x86\x01\n\x08\x43lanInfo\x12\x13\n\x0bmember_id_1\x18\x01 \x01(\x03\x12\x11\n\tclan_name\x18\x02 \x01(\t\x12\x13\n\x0bmember_id_2\x18\x03 \x01(\x03\x12\x12\n\nclan_level\x18\x04 \x01(\x05\x12\x0f\n\x07\x63lan_xp\x18\x05 \x01(\x05\x12\x18\n\x10\x63lan_xp_required\x18\x06 \x01(\x05\"\x89\x01\n\x0b\x41\x63hievement\x12\x16\n\x0e\x61\x63hievement_id\x18\x01 \x01(\x05\x12\x10\n\x08progress\x18\x03 \x01(\x05\x12\x15\n\rcurrent_level\x18\x04 \x01(\x05\x12\x11\n\treward_id\x18\x05 \x01(\x05\x12\x11\n\ttarget_id\x18\x06 \x01(\x05\x12\x13\n\x0bunlock_tier\x18\t \x01(\x05\"\x93\x01\n\x0cPlayerStatus\x12\x11\n\tstatus_id\x18\x01 \x01(\x05\x12\x17\n\x0funknown_field_2\x18\x02 \x01(\x05\x12\x14\n\x0cstatus_level\x18\x03 \x01(\x05\x12\x16\n\x0estatus_message\x18\t \x01(\t\x12\x14\n\x0cstatus_flags\x18\n \x01(\x05\x12\x13\n\x0b\x63ustom_data\x18\x0e \x01(\x0c\"\x19\n\x08\x43urrency\x12\r\n\x05\x63oins\x18\x01 \x01(\x05\"v\n\x10TimeLimitedEvent\x12\x10\n\x08\x65vent_id\x18\x01 \x01(\x05\x12\x17\n\x0funknown_field_3\x18\x03 \x01(\x05\x12\x12\n\nstart_time\x18\x08 \x01(\x03\x12\x10\n\x08\x65nd_time\x18\t \x01(\x03\x12\x11\n\tis_active\x18\n \x01(\x08\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'a_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CSGETPLAYERPERSONALSHOWRES']._serialized_start=19
  _globals['_CSGETPLAYERPERSONALSHOWRES']._serialized_end=341
  _globals['_PLAYERINFO']._serialized_start=344
  _globals['_PLAYERINFO']._serialized_end=1083
  _globals['_CLANTAG']._serialized_start=1085
  _globals['_CLANTAG']._serialized_end=1159
  _globals['_PREMIUMFEATURES']._serialized_start=1161
  _globals['_PREMIUMFEATURES']._serialized_end=1223
  _globals['_STATENTRY']._serialized_start=1225
  _globals['_STATENTRY']._serialized_end=1303
  _globals['_STATDETAIL']._serialized_start=1305
  _globals['_STATDETAIL']._serialized_end=1409
  _globals['_RECENTACTIVITY']._serialized_start=1411
  _globals['_RECENTACTIVITY']._serialized_end=1466
  _globals['_ACTIVITYENTRY']._serialized_start=1468
  _globals['_ACTIVITYENTRY']._serialized_end=1540
  _globals['_STATUSINDICATOR']._serialized_start=1542
  _globals['_STATUSINDICATOR']._serialized_end=1602
  _globals['_INVENTORY']._serialized_start=1605
  _globals['_INVENTORY']._serialized_end=1802
  _globals['_INVENTORYITEM']._serialized_start=1804
  _globals['_INVENTORYITEM']._serialized_end=1906
  _globals['_CLANINFO']._serialized_start=1909
  _globals['_CLANINFO']._serialized_end=2043
  _globals['_ACHIEVEMENT']._serialized_start=2046
  _globals['_ACHIEVEMENT']._serialized_end=2183
  _globals['_PLAYERSTATUS']._serialized_start=2186
  _globals['_PLAYERSTATUS']._serialized_end=2333
  _globals['_CURRENCY']._serialized_start=2335
  _globals['_CURRENCY']._serialized_end=2360
  _globals['_TIMELIMITEDEVENT']._serialized_start=2362
  _globals['_TIMELIMITEDEVENT']._serialized_end=2480
# @@protoc_insertion_point(module_scope)
