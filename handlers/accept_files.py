from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from loader import bot, channel_id
from states import AcceptState
from bot_buttons.reply import phone_button, start_menu_button
from bot_buttons.inline import accept_button, preview

accept_router = Router()

@accept_router.message(F.text == "Tanlovda ishtirok etish")
async def start_register(message: Message, state: FSMContext):
    await state.clear()
    text = """
Tanlovda ishtirok etish uchun
1. 👤To‘liq familiya, ism va sharifingiz (<i>masalan: Yodgorova Maftuna Erkin qizi</i>)
"""
    await message.answer(text)
    await state.set_state(AcceptState.full_name)


@accept_router.message(AcceptState.full_name)
async def get_full_name(message: Message, state: FSMContext):
    if len(message.text.strip()) < 8:
        return await message.answer("Juda qisqa yozdingiz, iltimos qayta urining")
    await state.update_data(full_name=message.text.strip())
    text = """
2. 📅Tug‘ilgan yilingizni kiriting (<i>masalan: 04.11.1999</i>)
"""
    await message.answer(text)
    await state.set_state(AcceptState.birth_date)


@accept_router.message(AcceptState.birth_date)
async def get_birth_date(message: Message, state: FSMContext):
    try:
        birth_date = datetime.strptime(message.text.strip(), "%d.%m.%Y")
    except ValueError:
        return await message.answer(
            "❌ Sana noto‘g‘ri formatda kiritildi. Iltimos to'g'ri kiriting\nMasalan: 04.11.1999"
        )

    await state.update_data(birth_date=message.text.strip())

    await message.answer(
        "3. 📸Fotosuratingizni yuboring (3×4)"
    )
    await state.set_state(AcceptState.image)


@accept_router.message(AcceptState.image)
async def get_image(message: Message, state: FSMContext):
    if not message.photo:
        return await message.answer("Iltimos rasm yuboring")
    
    photo_id = message.photo[-1].file_id
    await state.update_data(image=photo_id)

    await message.answer(
        "4. O‘qish yoki ish joyingizni kiriting\n"
        "(to‘liq nomi va manzili)"
    )
    await state.set_state(AcceptState.study_place)


@accept_router.message(AcceptState.study_place)
async def get_study_place(message: Message, state: FSMContext):
    await state.update_data(study_place=message.text.strip())

    await message.answer(
        "5. 📍Uy manzilingizni kiriting\n"
        "(masalan: Toshkent sh. Yunusobod, Bodomzor 10)"
    )
    await state.set_state(AcceptState.address)


@accept_router.message(AcceptState.address)
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text.strip())

    await message.answer("6. 📧Elektron pochta manzilingizni kiriting")
    await state.set_state(AcceptState.email)


@accept_router.message(AcceptState.email)
async def get_email(message: Message, state: FSMContext):
    if not message.text.endswith("@gmail.com"):
        return await message.answer("❌ Email noto‘g‘ri, qayta kiriting")

    await state.update_data(email=message.text.strip())

    await message.answer(
        "7. 📞Telefon raqamingizni yuboring",
        reply_markup=phone_button
    )
    await state.set_state(AcceptState.phone_number)


@accept_router.message(AcceptState.phone_number)
async def get_phone(message: Message, state: FSMContext):
    if message.contact:
        await state.update_data(phone_number=message.contact.phone_number)
    elif message.text and message.text.startswith("+998") and message.text[1:].isdigit():
        await state.update_data(phone_number=message.text)
    else:
        return await message.answer("❌ Telefon raqam noto‘g‘ri formatda")
    
    await message.answer(
        "8. Videorolik yoki hujjatni yuklang 🎥📁\n(Formatlar: MP4, PPTX)"
    )
    await state.set_state(AcceptState.file)


@accept_router.message(AcceptState.file)
async def get_file(message: Message, state: FSMContext):
    # Agar video yuborilgan bo'lsa
    if message.video:
        file_id = message.video.file_id
        await state.update_data(file_id=file_id, file_type="video")
        
    # Agar hujjat yuborilgan bo'lsa
    elif message.document:
        file_id = message.document.file_id
        await state.update_data(file_id=file_id, file_type="document")
        
    else:
        return await message.answer("Iltimos, video rolik yoki hujjat (MP4, PPTX) yuboring 🎥📁")

    data = await state.get_data()
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
    
    text = (
        "📥 Yangi ishtirokchi:\n\n"
        f"👤 F.I.Sh: {data['full_name']}\n"
        f"📱 Telegram: {username}\n"
        f"📅 Tug‘ilgan sana: {data['birth_date']}\n"
        f"🏫 Ish/O‘qish joyi: {data['study_place']}\n"
        f"🏠 Manzil: {data['address']}\n"
        f"📧 Email: {data['email']}\n"
        f"📞 Telefon: {data['phone_number']}\n\n"
        f"Barcha ma'lumotlaringizni tasdiqlaysizmi?"
    ) 

    # Foydalanuvchiga yuborilgan faylni ko'rsatish
    if data['file_type'] == "video":
        await message.answer_video(data['file_id'], caption="Yuborilgan video rolik 🎥")
    else:
        await message.answer_document(data['file_id'], caption="Yuborilgan hujjat 📁")
        
    # Anketa ma'lumotlarini rasm bilan tasdiqlashga chiqarish
    await message.answer_photo(data['image'], caption=text, reply_markup=preview)


@accept_router.callback_query(F.data.in_(["say_yes", "say_no"]))
async def accept_preview(callback: CallbackQuery, state: FSMContext):
    # Foydalanuvchi tugmani bosganda inline klaviaturani o'chirib yuboramiz
    await callback.message.edit_reply_markup(reply_markup=None)
    
    if callback.data == "say_no":
        await callback.message.answer("Bekor qilindi", reply_markup=start_menu_button)
        await state.clear()
        await callback.answer()
        
    elif callback.data == "say_yes":
        data = await state.get_data()
        file_id = data["file_id"]
        file_type = data["file_type"]
        username = f"@{callback.from_user.username}" if callback.from_user.username else "Mavjud emas"
        
        text = (    
            "📥 Yangi ishtirokchi:\n\n"
            f"👤 F.I.Sh: {data['full_name']}\n"
            f"📱 Telegram: {username}\n"
            f"📅 Tug‘ilgan sana: {data['birth_date']}\n"
            f"🏫 Ish/O‘qish joyi: {data['study_place']}\n"
            f"🏠 Manzil: {data['address']}\n"
            f"📧 Email: {data['email']}\n"
            f"📞 Telefon: {data['phone_number']}"
        )
    
        # Kanalga foydalanuvchi anketasini yuborish
        await bot.send_photo(channel_id, data["image"], caption=text)
        
        # Fayl turiga qarab kanalga mos ravishda video yoki document yuborish
        if file_type == "video":
            await bot.send_video(
                channel_id, 
                file_id, 
                caption="📹 Foydalanuvchining video roliki", 
                reply_markup=accept_button
            )
        else:
            await bot.send_document(
                channel_id, 
                file_id, 
                caption="📁 Foydalanuvchining hujjati", 
                reply_markup=accept_button
            )
    
        await callback.message.answer(
            "✅ Ma'lumotlar va video rolik qabul qilindi!",
            reply_markup=start_menu_button
        )
    
        await state.clear()
        await callback.answer()