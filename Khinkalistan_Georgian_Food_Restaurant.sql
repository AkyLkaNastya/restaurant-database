PGDMP                      |            georgian_food    17.2    17.2 +               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false                       1262    16481    georgian_food    DATABASE     �   CREATE DATABASE georgian_food WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE georgian_food;
                     postgres    false            k           1247    16630    units    TYPE     U   CREATE TYPE public.units AS ENUM (
    'liter',
    'kilogram',
    'single item'
);
    DROP TYPE public.units;
       public               postgres    false            �            1255    16735    chose_waiter()    FUNCTION     �  CREATE FUNCTION public.chose_waiter() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  serving_waiter VARCHAR(30);
BEGIN
  SELECT worker_name INTO serving_waiter
  FROM staff
  WHERE job_title = 'waiter'
  ORDER BY RANDOM()
  LIMIT 1;

  -- Обновляем NEW, чтобы установить значение для serving_waiter
  NEW.serving_waiter := serving_waiter;

  RETURN NEW;
END;
$$;
 %   DROP FUNCTION public.chose_waiter();
       public               postgres    false            �            1255    16825    generate_order_id()    FUNCTION     P  CREATE FUNCTION public.generate_order_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    existing_order_id INT;
    new_order_id INT;
    order_item_count INT;
BEGIN
    -- Проверяем, есть ли уже order_id у текущего заказа
    SELECT order_id INTO existing_order_id
    FROM order_positions
    WHERE order_id = NEW.order_id
    LIMIT 1;

    -- Получаем количество строк, которые будут вставлены для текущего заказа
    SELECT INTO order_item_count COUNT(*) FROM order_positions WHERE order_id = NEW.order_id;

    IF existing_order_id IS NULL OR order_item_count = 1 THEN
        -- Это новый заказ или первая строка существующего заказа
        SELECT COALESCE(MAX(order_id), 0) + 1 INTO new_order_id
        FROM order_positions;
        NEW.order_id := new_order_id;
    ELSE
        -- Это существующий заказ и не первая строка
        NEW.order_id := existing_order_id;
    END IF;

    RETURN NEW;
END;
$$;
 *   DROP FUNCTION public.generate_order_id();
       public               postgres    false            �            1255    16828    update_storage_after_order()    FUNCTION       CREATE FUNCTION public.update_storage_after_order() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    rec RECORD;
BEGIN
    -- Перебираем все ингредиенты для блюда, указанного в новой записи order_positions
    FOR rec IN 
        SELECT r.ingredient, r.ing_amount * NEW.amount AS required_amount
        FROM recipe r
        WHERE r.dish = NEW.dish
    LOOP
        -- Обновляем количество ингредиента в таблице storage
        UPDATE storage
        SET ingredient_left = ingredient_left - rec.required_amount
        WHERE ingredient = rec.ingredient;

        -- Проверяем, достаточно ли ингредиентов на складе
        IF (SELECT ingredient_left FROM storage WHERE ingredient = rec.ingredient) < 0 THEN
            RAISE EXCEPTION 'Недостаточно ингредиента "%" для блюда "%".', rec.ingredient, NEW.dish;
        END IF;
    END LOOP;

    RETURN NEW;
END;
$$;
 3   DROP FUNCTION public.update_storage_after_order();
       public               postgres    false            �            1255    16832 "   update_storage_with_new_supplies()    FUNCTION     �  CREATE FUNCTION public.update_storage_with_new_supplies() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.ingredient_left < 1 THEN
        UPDATE storage
        SET ingredient_left = ingredient_left + amount
        FROM supplies
        WHERE storage.ingredient = NEW.ingredient
        AND supplies.ingredient = NEW.ingredient;
    END IF;
    
    RETURN NEW;
END;
$$;
 9   DROP FUNCTION public.update_storage_with_new_supplies();
       public               postgres    false            �            1259    16500    menu    TABLE     /  CREATE TABLE public.menu (
    dish character varying(50) NOT NULL,
    price_usd numeric(4,0) NOT NULL,
    rating integer NOT NULL,
    stop_list boolean,
    CONSTRAINT menu_price_check CHECK ((price_usd > (0)::numeric)),
    CONSTRAINT menu_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);
    DROP TABLE public.menu;
       public         heap r       postgres    false            �            1259    16508    order_positions    TABLE     �   CREATE TABLE public.order_positions (
    order_id integer NOT NULL,
    dish character varying(50) NOT NULL,
    amount integer,
    position_number integer,
    CONSTRAINT order_positions_amount_check CHECK ((amount >= 0))
);
 #   DROP TABLE public.order_positions;
       public         heap r       postgres    false            �            1259    16490    orders    TABLE     �   CREATE TABLE public.orders (
    order_id integer NOT NULL,
    date date NOT NULL,
    total_cost numeric(5,0),
    serving_waiter character varying(255)
);
    DROP TABLE public.orders;
       public         heap r       postgres    false            �            1259    16675    recipe    TABLE     �   CREATE TABLE public.recipe (
    dish character varying(50) NOT NULL,
    ingredient character varying(30) NOT NULL,
    ing_amount numeric,
    units_of_measurement public.units
);
    DROP TABLE public.recipe;
       public         heap r       postgres    false    875            �            1259    16482    staff    TABLE     �  CREATE TABLE public.staff (
    worker_name character varying(50) NOT NULL,
    job_title character varying(100),
    salary_usd numeric(6,2) DEFAULT 2000.00,
    address character varying(200) NOT NULL,
    phone_number character(16),
    worker_id character varying(10),
    CONSTRAINT staff_job_title_check CHECK (((job_title)::text = ANY ((ARRAY['cook'::character varying, 'waiter'::character varying, 'barman'::character varying, 'chef'::character varying, 'manager'::character varying, 'security_guard'::character varying, 'cleaner'::character varying])::text[]))),
    CONSTRAINT staff_phone_number_check CHECK ((phone_number ~~ '+1-___-___-__-__'::text))
);
    DROP TABLE public.staff;
       public         heap r       postgres    false            �            1259    16524    storage    TABLE     1  CREATE TABLE public.storage (
    ingredient character varying(30) NOT NULL,
    ingredient_left numeric DEFAULT 0,
    max numeric,
    measurement_units_storage public.units,
    CONSTRAINT storage_check CHECK ((ingredient_left <= max)),
    CONSTRAINT storage_max_check CHECK ((max > (0)::numeric))
);
    DROP TABLE public.storage;
       public         heap r       postgres    false    875            �            1259    16547    supplier    TABLE     �  CREATE TABLE public.supplier (
    supplier_name character varying(50) NOT NULL,
    city character varying(50) NOT NULL,
    delivery character varying(10),
    contact_person character varying(100) NOT NULL,
    CONSTRAINT supplier_delivery_check CHECK (((delivery)::text = ANY ((ARRAY['truck'::character varying, 'van'::character varying, 'courier'::character varying])::text[])))
);
    DROP TABLE public.supplier;
       public         heap r       postgres    false            �            1259    16637    supplies    TABLE     y  CREATE TABLE public.supplies (
    measurement_units public.units,
    ingredient character varying(30) NOT NULL,
    amount numeric DEFAULT 0,
    price_in_usd numeric NOT NULL,
    supplier_name character varying(50) NOT NULL,
    CONSTRAINT supplies_amount_check CHECK ((amount >= (0)::numeric)),
    CONSTRAINT supplies_price_check CHECK ((price_in_usd > (0)::numeric))
);
    DROP TABLE public.supplies;
       public         heap r       postgres    false    875            �          0    16500    menu 
   TABLE DATA           B   COPY public.menu (dish, price_usd, rating, stop_list) FROM stdin;
    public               postgres    false    219   �B       �          0    16508    order_positions 
   TABLE DATA           R   COPY public.order_positions (order_id, dish, amount, position_number) FROM stdin;
    public               postgres    false    220   ^C       �          0    16490    orders 
   TABLE DATA           L   COPY public.orders (order_id, date, total_cost, serving_waiter) FROM stdin;
    public               postgres    false    218   �C                 0    16675    recipe 
   TABLE DATA           T   COPY public.recipe (dish, ingredient, ing_amount, units_of_measurement) FROM stdin;
    public               postgres    false    224   �C       �          0    16482    staff 
   TABLE DATA           e   COPY public.staff (worker_name, job_title, salary_usd, address, phone_number, worker_id) FROM stdin;
    public               postgres    false    217   �E       �          0    16524    storage 
   TABLE DATA           ^   COPY public.storage (ingredient, ingredient_left, max, measurement_units_storage) FROM stdin;
    public               postgres    false    221   )G                  0    16547    supplier 
   TABLE DATA           Q   COPY public.supplier (supplier_name, city, delivery, contact_person) FROM stdin;
    public               postgres    false    222   JH                 0    16637    supplies 
   TABLE DATA           f   COPY public.supplies (measurement_units, ingredient, amount, price_in_usd, supplier_name) FROM stdin;
    public               postgres    false    223   ,I       U           2606    16507    menu menu_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.menu
    ADD CONSTRAINT menu_pkey PRIMARY KEY (dish);
 8   ALTER TABLE ONLY public.menu DROP CONSTRAINT menu_pkey;
       public                 postgres    false    219            W           2606    16513 $   order_positions order_positions_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY public.order_positions
    ADD CONSTRAINT order_positions_pkey PRIMARY KEY (order_id, dish);
 N   ALTER TABLE ONLY public.order_positions DROP CONSTRAINT order_positions_pkey;
       public                 postgres    false    220    220            S           2606    16494    orders orders_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public                 postgres    false    218            `           2606    16681    recipe recipe_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.recipe
    ADD CONSTRAINT recipe_pkey PRIMARY KEY (ingredient, dish);
 <   ALTER TABLE ONLY public.recipe DROP CONSTRAINT recipe_pkey;
       public                 postgres    false    224    224            Q           2606    16489    staff staff_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_pkey PRIMARY KEY (worker_name);
 :   ALTER TABLE ONLY public.staff DROP CONSTRAINT staff_pkey;
       public                 postgres    false    217            Y           2606    16531    storage storage_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.storage
    ADD CONSTRAINT storage_pkey PRIMARY KEY (ingredient);
 >   ALTER TABLE ONLY public.storage DROP CONSTRAINT storage_pkey;
       public                 postgres    false    221            [           2606    16552    supplier supplier_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.supplier
    ADD CONSTRAINT supplier_pkey PRIMARY KEY (supplier_name);
 @   ALTER TABLE ONLY public.supplier DROP CONSTRAINT supplier_pkey;
       public                 postgres    false    222            ^           2606    16646    supplies supplies_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.supplies
    ADD CONSTRAINT supplies_pkey PRIMARY KEY (ingredient);
 @   ALTER TABLE ONLY public.supplies DROP CONSTRAINT supplies_pkey;
       public                 postgres    false    223            \           1259    16834    suppliers_index    INDEX     T   CREATE UNIQUE INDEX suppliers_index ON public.supplier USING btree (supplier_name);
 #   DROP INDEX public.suppliers_index;
       public                 postgres    false    222            g           2620    16829 "   order_positions after_order_insert    TRIGGER     �   CREATE TRIGGER after_order_insert AFTER INSERT ON public.order_positions FOR EACH ROW EXECUTE FUNCTION public.update_storage_after_order();
 ;   DROP TRIGGER after_order_insert ON public.order_positions;
       public               postgres    false    220    238            h           2620    16826 4   order_positions generate_order_id_on_order_positions    TRIGGER     �   CREATE TRIGGER generate_order_id_on_order_positions BEFORE INSERT ON public.order_positions FOR EACH ROW EXECUTE FUNCTION public.generate_order_id();
 M   DROP TRIGGER generate_order_id_on_order_positions ON public.order_positions;
       public               postgres    false    220    237            i           2620    16833 0   storage update_storage_with_new_supplies_trigger    TRIGGER     �   CREATE TRIGGER update_storage_with_new_supplies_trigger AFTER UPDATE OF ingredient_left ON public.storage FOR EACH ROW EXECUTE FUNCTION public.update_storage_with_new_supplies();
 I   DROP TRIGGER update_storage_with_new_supplies_trigger ON public.storage;
       public               postgres    false    221    221    239            a           2606    16697    orders create_bond    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT create_bond FOREIGN KEY (serving_waiter) REFERENCES public.staff(worker_name);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT create_bond;
       public               postgres    false    4689    218    217            b           2606    16519 )   order_positions order_positions_dish_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_positions
    ADD CONSTRAINT order_positions_dish_fkey FOREIGN KEY (dish) REFERENCES public.menu(dish);
 S   ALTER TABLE ONLY public.order_positions DROP CONSTRAINT order_positions_dish_fkey;
       public               postgres    false    220    219    4693            e           2606    16687    recipe recipe_dish_fkey    FK CONSTRAINT     t   ALTER TABLE ONLY public.recipe
    ADD CONSTRAINT recipe_dish_fkey FOREIGN KEY (dish) REFERENCES public.menu(dish);
 A   ALTER TABLE ONLY public.recipe DROP CONSTRAINT recipe_dish_fkey;
       public               postgres    false    224    4693    219            f           2606    16682    recipe recipe_ingredient_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.recipe
    ADD CONSTRAINT recipe_ingredient_fkey FOREIGN KEY (ingredient) REFERENCES public.storage(ingredient);
 G   ALTER TABLE ONLY public.recipe DROP CONSTRAINT recipe_ingredient_fkey;
       public               postgres    false    224    221    4697            c           2606    16647 !   supplies supplies_ingredient_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.supplies
    ADD CONSTRAINT supplies_ingredient_fkey FOREIGN KEY (ingredient) REFERENCES public.storage(ingredient);
 K   ALTER TABLE ONLY public.supplies DROP CONSTRAINT supplies_ingredient_fkey;
       public               postgres    false    221    4697    223            d           2606    16652 $   supplies supplies_supplier_name_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.supplies
    ADD CONSTRAINT supplies_supplier_name_fkey FOREIGN KEY (supplier_name) REFERENCES public.supplier(supplier_name);
 N   ALTER TABLE ONLY public.supplies DROP CONSTRAINT supplies_supplier_name_fkey;
       public               postgres    false    223    4699    222            �   �   x�e��
�0D��W�HEz��z(F��˶n�Ҧ[Br��-�"��7�TDԖ�'VU�A_�u?v�Xm���D�J��݈��ұ�}�O���=�噠�&R�bs�qk9P&��`$z�xBcO���8�!�p��,H�;��ȄA�      �   c   x�3��/�V�����N���4���2�.�L�T��M,�WN,MN�4�szg$&g$�er�DL�`�� 3�1D,0D�Yb��b���� [�D�      �      x������ � �         �  x����R�0���y�T��Z���Xgz��2�&��}{؆�$�c�����-����5�'LI"8<�ˤ%������y��l�<�>i$[%'BE%������ ѐZ��w�;cr�Eu'�	��ӊ��>��S�q�����yì0a�ON'6�cw*��k3>����qY㦓�W�Vd��5@=���o2_~eNSw\�>�D�О��s�*�mDA�.v�pA`ގ����J��G7TI��U������`<=UXRR��a��Z^	�t}��	�JQH����l_����8OwZ�}6��J�x�`ty���PM3/����U<�mm�y����L�y(Eؕ?������Ufײ�E�_�?GP�/�sLƍ�����
.����8�&�7I��H���vP      �     x�}�Qo� �g�)�}&�c󘭛�vY[MS5i�t���J`,���H�K&�x�����c�=ܢ�#Gt��@$cl���w�p��]��ˇ���a�6�U���)��5��&;�x�t�n2>y���q 3�t���a���w�.ް����a��AEQP^R.�s���8��?���f���~�3�����|�0& Z���:��hɢ�(��G"w�4bjA�_��_�b�KJ^%R�ےJ��"�l���O�@�F���~���{��.������⊖��2�"{��-�k��[C����
y�o.9����!`0�֡��g�T\���=�<뻎��GFݜ���?�	CKDy��G<bo�58H�z�F�8-Ds�m�j���M�e�����      �     x�]Q�n�0<���_��Q����\r1�1+�@����4�j8zfv<;�#>A���0��:(ˌ�=th�a!�w�45��Fr� ���i|B5�l���Nު�w+Q��4:|������J�
(0Kf�e5��X�_pY0�ƣ_*��BFn�+[�"�U/������V�?q�wr��(���ܧ�|�Dwmʸ5E��FO�sBW]-Ge4U��C�aB��DS]�Ħr���z�i����e��dv;���I�z�(OwzT��o�֧"          �   x�M��j�0���S���N�H�4-����R(��֢[	�R���u&���7?��'V{��>#���:�:`f�D�u����`������/Ψ�\�o�*�8".)�����׀n��^�4������1O☢��|��;�I��Y�z��ųft�N��xv����wB�֋g��/H�������}qmzuT.��덅��nAw��AJ���W�         P  x����N�@���S��wj�����B/t�2">�=�5YB`���H�ƃ;Ľ��|����s���M�}��]ԯҲ�K��F�����*P����iݐ�Xݤ�7zYy�Gf�t��Z�Ô�t�^sP�E5���_�=`���$g���G�o�k�d�P������.Ɨ��0!�ǾGנ���x1A�sy����[�5��`�Z�_\-�eB/i�-�
�騶8��q�'��`�Vd�ș���kz�a<��|�z��COi�u���'��F#���[���<�z������l[~]L��cz9˲��$#�     