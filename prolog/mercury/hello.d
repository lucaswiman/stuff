

hello.optdate hello.trans_opt_date hello.err hello.c_date hello.s_date hello.pic_s_date hello.il_date hello.java_date : hello.m

hello.mh hello.mih : hello.c


ifeq ($(findstring il,$(GRADE)),il)
hello.module_dep : hello.il
else
 ifeq ($(findstring java,$(GRADE)),java)
hello.module_dep : jmercury/hello.java
 else
hello.module_dep : hello.c
 endif
endif


hello.date hello.date0 : hello.m

hello.date0 : hello.m


hello.int0 : hello.date0
	@:
hello.int : hello.date
	@:
hello.int2 : hello.date
	@:
hello.int3 : hello.date3
	@:
hello.opt : hello.optdate
	@:
hello.trans_opt : hello.trans_opt_date
	@:
