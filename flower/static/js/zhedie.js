/**
 * Created by sws on 5/9/17.
 * JSON无限折叠菜单
 * @constructor {AccordionMenu}
 * @param {options} 对象
 */

 function AccordionMenu(options) {
    this.config = {
        containerCls        : '.wrap-menu',                // 外层容器
        menuArrs            :  '',                         //  JSON传进来的数据
        type                :  'click',                    // 默认为click 也可以mouseover
        renderCallBack      :  null,                       // 渲染html结构后回调
        clickItemCallBack   : null                         // 每点击某一项时候回调
    };
    this.cache = {

    };
    this.init(options);
 }

 AccordionMenu.prototype = {
    constructor: AccordionMenu,
    init: function(options){
        this.config = $.extend(this.config,options || {});
        var self = this,
            _config = self.config,
            _cache = self.cache;

        // 渲染html结构
        $(_config.containerCls).each(function(index,item){

            self._renderHTML(item);
            // 处理点击事件
            self._bindEnv(item);
        });
    },
    _renderHTML: function(container){
        var self = this,
            _config = self.config,
            _cache = self.cache;
        var ulhtml = $('<ul></ul>');
        //$(_config.menuArrs).each(function(index,item){
        //    //console.log("123");
        //    //console.log(item);
        item  = _config.menuArrs
            if(item instanceof Array && item.length > 0) {
                for (var oo in item) {  // 本身是一个数组

                    if (item[oo] instanceof Array && item[oo].length > 0) {
                        var lihtml = $('<li><h2>' + "[...]" + '</h2></li>');
                        self._createSubMenu(item[oo], lihtml);
                    }
                    else if (item[oo] instanceof Object) {
                        var lihtml = $('<li><h2 >' + "{...}" + '</h2></li>');
                        self._createSubMenu(item[oo], lihtml);
                    }
                    else {
                        var lihtml = $('<li><h2>' + "" + item[oo] + '</h2></li>');
                    }
                    $(ulhtml).append(lihtml);
                }
            }
            else if(item instanceof Object) {
                for (var oo in item) {  // 本身是一个字典
                    if (item[oo] instanceof Array && item[oo].length > 0) {
                    var lihtml = $('<li><h2 >' + oo +"[...]" + '</h2></li>');
                    self._createSubMenu(item[oo], lihtml);
                    }
                    else if (item[oo] instanceof Object) {

                        var lihtml = $('<li><h2>' + oo + "{...}" + '</h2></li>');
                        self._createSubMenu(item[oo], lihtml);
                    }
                    else {
                        var lihtml = $('<li><h2>' + oo + "" + item[oo] + '</h2></li>');
                    }
                    $(ulhtml).append(lihtml);
                }

            }
            else{
                var lihtml = $('<li><h2>' + oo + "" + item[oo] + '</h2></li>');
                $(ulhtml).append(lihtml);
            }
            //var lihtml = $('<li><h2>'+item.name+'</h2></li>');
            //if(item.submenu && item.submenu.length > 0) {
            //    self._createSubMenu(item.submenu,lihtml);
            //}
            //$(ulhtml).append(lihtml);
        //});
        $(container).append(ulhtml);

        _config.renderCallBack && $.isFunction(_config.renderCallBack) && _config.renderCallBack();

        // 处理层级缩进
        self._levelIndent(ulhtml);
    },
    /**
     * 创建子菜单
     * @param {array} 子菜单
     * @param {lihtml} li项
     */
    _createSubMenu: function(submenu,lihtml){
        var self = this,
            _config = self.config,
            _cache = self.cache;
        var subUl = $('<ul></ul>'),
            callee = arguments.callee,
            subLi;

        //$(submenu).each(function(index,item){
        //console.log(submenu);
        //console.log(submenu instanceof Array);
            if (submenu instanceof Array ) {
                for (var oo in submenu) {
                    //var url = item.url || 'javascript:void(0)';
                    ////console.log(item[oo]);
                    ////console.log(item[oo] instanceof Object);
                    if (submenu[oo] instanceof Array) {  // 处理数组中的数组
                        subLi = $('<li><a class="btn btn-default" href="javascript:void(0)>' + submenu[oo] + '</a></li>');
                        $(subLi).children('a').prepend('<img  alt=""/>');
                        callee(submenu[oo], subLi);
                        $(subUl).append(subLi);
                    }
                    else if (submenu[oo] instanceof Object ){  //处理数组中的字典
                        subLi = $('<li><a class="btn btn-default" href="javascript:void(0)">'  +"{...}"+ '</a></li>');
                        $(subLi).children('a').prepend('<img  alt=""/>');
                        $(subUl).append(subLi);
                        callee(submenu[oo], subLi);
                        $(subUl).append(subLi);

                        ////console.log(sub);
                        ////console.log("sasas");
                    }
                    else { // 处理数组中的元素
                        subLi = $('<li><a class="btn btn-default" >' +submenu[oo]+ '</a></li>');
                        ////console.log(subLi);
                        $(subUl).append(subLi);
                    }

                }
            }
            else if (submenu instanceof Object){
                //console.log(submenu['rr']);
                //console.log(123);
                for (var oo in submenu) {
                    //var url = item.url || 'javascript:void(0)';
                    //console.log(submenu[oo]);
                    //console.log(oo);
                    ////console.log(item[oo] instanceof Object);
                    if (submenu[oo] instanceof Array) {  // 处理字典中的数组
                        subLi = $('<li><a class="btn btn-default" href="javascript:void(0)">' + oo +":"+ "[...]" + '</a></li>');
                        $(subLi).children('a').prepend('<img  alt=""/>');
                        callee(submenu[oo], subLi);
                        $(subUl).append(subLi);
                    }
                    else if (submenu[oo] instanceof Object){  //处理字典中的字典
                        subLi = $('<li><a class="btn btn-default" >' +oo +":{...}"+ '</a></li>');
                        $(subLi).children('a').prepend('<img  alt=""/>');

                        callee(submenu[oo], subLi);
                        $(subUl).append(subLi);

                        ////console.log(item[oo]);
                        ////console.log("sasas");
                    }
                    else { // 处理字典中的元素
                        subLi = $('<li><a class="btn btn-default" >' + oo +":"+ submenu[oo]+ '</a></li>');
                        //console.log(submenu instanceof Array);
                        //console.log(submenu);
                        //console.log(oo);

                        $(subUl).append(subLi);
                    }

                    //$(subUl).append(subLi);
                }
            }
            else {
                    subLi = $('<li><a class="btn btn-default" >' + submenu + '</a></li>');
                    if (submenu instanceof Array && submenu.length > 0) {
                        $(subLi).children('a').prepend('<img  alt=""/>');
                        callee(submenu[oo], subLi);
                        //$(subUl).append(subLi);
                    }
                    $(subUl).append(subLi);
            }

        $(lihtml).append(subUl);
    },
    /**
     * 处理层级缩进
     */
    _levelIndent: function(ulList){
        var self = this,
            _config = self.config,
            _cache = self.cache,
            callee = arguments.callee;

        var initTextIndent = 2,
            lev = 1,
            $oUl = $(ulList);

        while($oUl.find('ul').length > 0){
            initTextIndent = parseInt(initTextIndent,10) + 2 + 'em';
            $oUl.children().children('ul').addClass('lev-' + lev)
                        .children('li')//.css('text-indent', initTextIndent);
            $oUl = $oUl.children().children('ul');
            lev++;
        }
        $(ulList).find('ul').hide();
        //$(ulList).find('ul:first').show();
    },
    /**
     * 绑定事件
     */
    _bindEnv: function(container) {
        var self = this,
            _config = self.config;
        $('h2,a',container).unbind(_config.type);
        $('h2,a',container).bind(_config.type,function(e){
            if($(this).siblings('ul').length > 0) {
                $(this).siblings('ul').slideToggle('slow').end().children('img').toggleClass('unfold');
            }
            $(this).parent('li').siblings().find('ul').hide()
                   .end().find('img.unfold').removeClass('unfold');
            _config.clickItemCallBack && $.isFunction(_config.clickItemCallBack) && _config.clickItemCallBack($(this));
        });
    }
 };