from fastapi import FastAPI, APIRouter, status, HTTPException
from pydantic import BaseModel, RootModel
from typing import Optional, List


app = FastAPI(
    title="Courses Management API",
    description="API для управления учебными курсами",
    version="1.0.0"
)

courses_router = APIRouter(
    prefix="/api/v1/courses",
    tags=["courses-service"]
)


class CourseIn(BaseModel):
    """
    Входная модель курса для создания и обновления.
    Не содержит поле id, так как оно генерируется автоматически.
    """
    title: str
    max_score: int
    min_score: int
    description: str


class CourseOut(CourseIn):
    """
    Выходная модель курса, включающая автоматически сгенерированный id.
    Наследует все поля от CourseIn и добавляет поле id.
    """
    id: int


class CoursesStore(RootModel):
    """
    In-memory хранилище курсов на основе Pydantic RootModel.
    Хранит все данные в оперативной памяти в виде списка курсов.
    """
    root: List[CourseOut] = []
    
    def find(self, course_id: int) -> Optional[CourseOut]:
        """
        Находит курс по его ID.
        
        Args:
            course_id: Идентификатор курса для поиска
            
        Returns:
            Найденный курс или None, если курс не существует
        """
        for course in self.root:
            if course.id == course_id:
                return course
        return None
    
    def create(self, course_in: CourseIn) -> CourseOut:
        """
        Создает новый курс с автоматически сгенерированным ID.
        
        Args:
            course_in: Данные для создания нового курса
            
        Returns:
            Созданный курс с присвоенным ID
        """
        new_id = max([course.id for course in self.root], default=0) + 1
        
        course_out = CourseOut(
            id=new_id,
            **course_in.model_dump()
        )
        
        self.root.append(course_out)
        
        return course_out
    
    def update(self, course_id: int, course_in: CourseIn) -> Optional[CourseOut]:
        """
        Обновляет существующий курс по его ID.
        
        Args:
            course_id: Идентификатор курса для обновления
            course_in: Новые данные для курса
            
        Returns:
            Обновленный курс или None, если курс не найден
        """
        for i, course in enumerate(self.root):
            if course.id == course_id:
                updated_course = CourseOut(
                    id=course_id,
                    **course_in.model_dump()
                )
                self.root[i] = updated_course
                return updated_course
        return None
    
    def delete(self, course_id: int) -> bool:
        """
        Удаляет курс по его ID.
        
        Args:
            course_id: Идентификатор курса для удаления
            
        Returns:
            True, если курс был удален, False, если курс не найден
        """
        initial_length = len(self.root)
        
        self.root = [course for course in self.root if course.id != course_id]
        
        return len(self.root) < initial_length


store = CoursesStore(root=[])


@courses_router.get(
    "/{course_id}",
    response_model=CourseOut,
    summary="Получить курс по ID",
    description="Возвращает информацию о курсе по указанному идентификатору."
)
async def get_course(course_id: int):
    """
    Получить информацию о курсе по его идентификатору.
    
    Args:
        course_id: Идентификатор курса
        
    Returns:
        Информация о курсе
        
    Raises:
        HTTPException: 404, если курс с указанным ID не найден
    """
    course = store.find(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return course


@courses_router.get(
    "",
    response_model=List[CourseOut],
    summary="Получить все курсы",
    description="Возвращает список всех курсов в системе."
)
async def get_courses():
    """
    Получить список всех курсов.
    
    Returns:
        Список всех курсов
    """
    return store.root


@courses_router.post(
    "",
    response_model=CourseOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый курс",
    description="Создает новый курс с автоматически сгенерированным ID."
)
async def create_course(course_in: CourseIn):
    """
    Создать новый курс.
    
    Args:
        course_in: Данные для создания нового курса
        
    Returns:
        Созданный курс с присвоенным ID
    """
    return store.create(course_in)


@courses_router.put(
    "/{course_id}",
    response_model=CourseOut,
    summary="Обновить курс",
    description="Обновляет информацию о курсе по указанному идентификатору."
)
async def update_course(course_id: int, course_in: CourseIn):
    """
    Обновить информацию о курсе.
    
    Args:
        course_id: Идентификатор курса для обновления
        course_in: Новые данные для курса
        
    Returns:
        Обновленный курс
        
    Raises:
        HTTPException: 404, если курс с указанным ID не найден
    """
    existing_course = store.find(course_id)
    if not existing_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    
    updated_course = store.update(course_id, course_in)
    
    return updated_course


@courses_router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить курс",
    description="Удаляет курс по указанному идентификатору."
)
async def delete_course(course_id: int):
    """
    Удалить курс.
    
    Args:
        course_id: Идентификатор курса для удаления
        
    Raises:
        HTTPException: 404, если курс с указанным ID не найден
    """
    existing_course = store.find(course_id)
    if not existing_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    
    store.delete(course_id)
    


# Подключаем роутер к приложению
app.include_router(courses_router)